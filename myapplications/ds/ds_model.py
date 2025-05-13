import pandas as pd
from pathlib import Path  
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

def calculate_retention_rate(rfm_df, churn_threshold=90):
    total_customers = rfm_df.shape[0]
    churned_customers = rfm_df[rfm_df["Recency"] > churn_threshold].shape[0]
    return (1 - churned_customers / total_customers) * 100

def save_dfs_to_postgres(clv_df: pd.DataFrame, rfm_df: pd.DataFrame):
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path=env_path)
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    engine = create_engine(database_url)

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

def process_dataset(data_dir: Path):
    print(f"\n📁 Processing folder: {data_dir.name}")

    # Load CSVs
    attendance = pd.read_csv(data_dir / 'attendance.csv')
    customers = pd.read_csv(data_dir / 'customers.csv')
    gyms = pd.read_csv(data_dir / 'gyms.csv')
    packages = pd.read_csv(data_dir / 'packages.csv')
    transactions = pd.read_csv(data_dir / 'transactions.csv')

    attendance['check_out'] = pd.to_datetime(attendance['check_out'])
    transactions['date'] = pd.to_datetime(transactions['date'])
    reference_date = attendance['check_out'].max()

    # RFM Modeling 
    rfm = attendance.groupby('customer_id').agg({
        'check_out': lambda x: (reference_date - x.max()).days,
        'customer_id': 'count'
    }).rename(columns={'check_out': 'Recency', 'customer_id': 'Frequency'}).reset_index()

    monetary = transactions.groupby('customer_id')['amount'].sum().reset_index()
    monetary.columns = ['customer_id', 'Monetary']
    rfm = rfm.merge(monetary, on='customer_id', how='left')
    rfm['Monetary'] = rfm['Monetary'].fillna(0)

    # Scaling Data for KMeans
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    # Applying KMeans
    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm['Segment'] = kmeans.fit_predict(rfm_scaled)

    # Segment naming
    segment_mapping = {
        0: 'Loyalist',
        1: 'At Risk',
        2: 'New/Potential',
        3: 'High-Value'
    }
    rfm['Segment'] = rfm['Segment'].map(segment_mapping)

    # CLV Estimations
    # # CLV is calculated based on this formula: CLV = Average Order Value × Purchase Frequency × Average Customer Lifespan
    transactions['order_count'] = 1
    aov = transactions.groupby('customer_id').agg({
        'amount': 'sum',
        'order_count': 'count'
    }).eval('AOV = amount / order_count')
    rfm = rfm.merge(aov['AOV'], on='customer_id', how='left')
    rfm['CLV'] = rfm['AOV'] * rfm['Frequency'] * 1
    rfm = rfm.fillna({'AOV': 0, 'CLV': 0})

    # Save RFM + CLV DataFrames
    clv_df = rfm[["customer_id", "CLV", "AOV", "Segment"]].rename(columns={
        "CLV": "clv_value",
        "AOV": "average_order_value",
        "Segment": "predicted_customer_type"
    }).copy()
    clv_df.insert(0, "clv_id", range(1, len(clv_df) + 1))

    rfm_df = rfm[["customer_id", "Recency", "Frequency", "Monetary", "Segment"]].rename(columns={
        "Recency": "recency_score",
        "Frequency": "frequency_score",
        "Monetary": "monetary_score",
        "Segment": "customer_segment"
    }).copy()
    rfm_df.insert(0, "rfm_id", range(1, len(rfm_df) + 1))

    # Retention rate
    retention = calculate_retention_rate(rfm)
    print(f"Retention Rate: {retention:.2f}%")

    # Push to PostgreSQL
    save_dfs_to_postgres(clv_df, rfm_df)
    print("The model output is pushed to the Database.")


# MAIN EXECUTION
if __name__ == "__main__":
    current_dir = Path(__file__).parent
    parent_data_dir = current_dir.parent / 'etl' / 'data'
    process_dataset(parent_data_dir)
