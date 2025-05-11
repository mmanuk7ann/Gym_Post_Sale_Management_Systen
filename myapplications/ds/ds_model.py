import pandas as pd
from pathlib import Path  
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os


current_dir = Path(__file__).parent

# Constructing paths to the CSV files
data_dir = current_dir.parent / 'etl' / 'data'

# Loading each CSV file
attendance = pd.read_csv(data_dir / 'attendance.csv')
customers = pd.read_csv(data_dir / 'customers.csv')
gyms = pd.read_csv(data_dir / 'gyms.csv')
packages = pd.read_csv(data_dir / 'packages.csv')
transactions = pd.read_csv(data_dir / 'transactions.csv')


# Converting date columns
attendance['check_out'] = pd.to_datetime(attendance['check_out'])
transactions['date'] = pd.to_datetime(transactions['date'])

reference_date = attendance['check_out'].max()

# RFM Metrics
rfm = attendance.groupby('customer_id').agg({
    'check_out': lambda x: (reference_date - x.max()).days,
    'customer_id': 'count'
}).rename(columns={'check_out': 'Recency', 'customer_id': 'Frequency'}).reset_index()

monetary = transactions.groupby('customer_id')['amount'].sum().reset_index()
monetary.columns = ['customer_id', 'Monetary']
rfm = rfm.merge(monetary, on='customer_id', how='left')
rfm['Monetary'] = rfm['Monetary'].fillna(0)


# Scaling RFM values
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

# Elbow method to determine optimal number of clusters
sse = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(rfm_scaled)
    sse.append(km.inertia_)

# Plot of the Elbow curve
plt.figure(figsize=(8, 4))
plt.plot(k_range, sse, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('SSE (Inertia)')
plt.title('Elbow Method For Optimal k')
plt.grid(True)
#plt.show()
# According to the plot the optimal number of clusters is 4

# Fitting KMeans with k = 4
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Segment'] = kmeans.fit_predict(rfm_scaled)


segment_summary = rfm.groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'customer_id': 'count'
}).rename(columns={'customer_id': 'Count'}).reset_index()

print(segment_summary)

# Average Order Value (AOV) per customer
transactions['order_count'] = 1
aov = transactions.groupby('customer_id').agg({
    'amount': 'sum',
    'order_count': 'count'
}).eval('AOV = amount / order_count')

# Merging with Frequency
rfm = rfm.merge(aov['AOV'], on='customer_id', how='left')

# Estimating CLV 
rfm['CLV'] = rfm['AOV'] * rfm['Frequency'] * 1  # 1 = assumed lifespan (years)
rfm = rfm.fillna({'AOV': 0, 'CLV': 0}) # For the customers who haven't 


# CLV is calculated based on this formula: CLV = Average Order Value × Purchase Frequency × Average Customer Lifespan

# By analyzing the mean RFM values per segment and comparing them with the CLV values we can see:
# Segment 0 - Loyalists
# Segment 1 - At Risk Customers
# Segment 2 - New/Potenttial Customers
# Segment 0 - High-Value Customers

# Segment mapping 
segment_mapping = {
    0: 'Loyalist',
    1: 'At Risk',
    2: 'New/Potential',
    3: 'High-Value'
}
rfm['Segment'] = rfm['Segment'].map(segment_mapping)

print(rfm)


# Saving Results to new DataFrames

clv_df = rfm[["customer_id", "CLV", "AOV", "Segment"]].copy()
clv_df = clv_df.rename(columns={
    "CLV": "clv_value",
    "AOV": "average_order_value",
    "Segment": "predicted_customer_type"
})
clv_df.insert(0, "clv_id", range(1, len(clv_df) + 1))  # auto-increment ID

# Saving clv.csv
#clv_df.to_csv(data_dir / "clv.csv", index=False)


rfm_df = rfm[["customer_id", "Recency", "Frequency", "Monetary", "Segment"]].copy()
rfm_df = rfm_df.rename(columns={
    "Recency": "recency_score",
    "Frequency": "frequency_score",
    "Monetary": "monetary_score",  
    "Segment": "customer_segment"
})
rfm_df.insert(0, "rfm_id", range(1, len(rfm_df) + 1))  # auto-increment ID

# Saving rfm.csv
#rfm_df.to_csv(data_dir / "rfm.csv", index=False)



# Calculating Retention Rate

def calculate_retention_rate(rfm_df, churn_threshold=90):
    """
    Calculate retention rate based on a recency threshold.

    """
    total_customers = rfm_df.shape[0]
    churned_customers = rfm_df[rfm_df["Recency"] > churn_threshold].shape[0]

    retention_rate = (1 - churned_customers / total_customers) * 100
    return retention_rate


retention = calculate_retention_rate(rfm)
print(f"Retention Rate: {retention:.2f}%")



def save_dfs_to_postgres(clv_df: pd.DataFrame, rfm_df: pd.DataFrame):
    """
    Pushes clv_df and rfm_df to a PostgreSQL database 
    """
    # Load environment variables from the parent directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path=env_path)

    # Get the database connection URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    # Create database engine
    engine = create_engine(database_url)

    # Save dataframes to the database
    try:
        clv_df.to_sql('clv', con=engine, if_exists='replace', index=False)
        print("clv_df inserted into 'clv' table.")
    except Exception as e:
        print(f"Error inserting clv_df: {e}")

    try:
        rfm_df.to_sql('rfm', con=engine, if_exists='replace', index=False)
        print("rfm_df inserted into 'rfm' table.")
    except Exception as e:
        print(f"Error inserting rfm_df: {e}")


save_dfs_to_postgres(clv_df, rfm_df)