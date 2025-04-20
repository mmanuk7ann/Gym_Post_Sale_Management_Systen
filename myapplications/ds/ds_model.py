from etl.Database.database import SessionLocal
from etl.Database.helpers import get_active_customers
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def run_clustering():
    # Get data using CRUD helper
    db = SessionLocal()
    customers = get_active_customers(db)
    db.close()

    if not customers:
        print("No customers found.")
        return []

    # Convert to DataFrame
    df = pd.DataFrame([cust._dict_ for cust in customers])
    df.drop(columns=["_sa_instance_state", "email", "name", "gender", "phone"], errors="ignore", inplace=True)

    # Add simulated features for modeling
    df["visits_last_month"] = [10, 8, 12, 4, 9][:len(df)]
    df["total_spent"] = [150, 200, 300, 120, 250][:len(df)]

    # Preprocess and run KMeans
    features = df[["visits_last_month", "total_spent"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    print(df[["customer_id", "visits_last_month", "total_spent", "cluster"]])

    return df[["customer_id", "cluster"]].to_dict(orient="records")