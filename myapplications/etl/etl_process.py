"""
ETL Script for Generating and Loading Gym Data into Database.
"""
import os
import pandas as pd
from loguru import logger
import random
import glob
from os import path

from Database.models import *
from Database.database import engine
from Database.data_generator import (
    generate_gym,
    generate_package,
    generate_customer,
    generate_transaction,
    generate_attendance
)

# -----------------------------------------------------
# Constants
# -----------------------------------------------------
NUM_GYMS = 3
NUM_PACKAGES = 6
NUM_CUSTOMERS = 20
NUM_TRANSACTIONS = 30
NUM_ATTENDANCES = 40

# -----------------------------------------------------
# Generate & Save Data
# -----------------------------------------------------

# Create folders if needed
os.makedirs("data", exist_ok=True)

# Generate gyms
gyms = pd.DataFrame([generate_gym(gym_id) for gym_id in range(1, NUM_GYMS + 1)])
gyms.to_csv("data/gyms.csv", index=False)
logger.info(f"Gyms: {gyms.shape}")

# Generate packages
packages = pd.DataFrame([
    generate_package(package_id, random.randint(1, NUM_GYMS))
    for package_id in range(1, NUM_PACKAGES + 1)
])
packages.to_csv("data/packages.csv", index=False)
logger.info(f"Packages: {packages.shape}")

# Generate customers
customers = pd.DataFrame([
    generate_customer(cust_id, random.randint(1, NUM_GYMS), random.randint(1, NUM_PACKAGES))
    for cust_id in range(1, NUM_CUSTOMERS + 1)
])
customers.to_csv("data/customers.csv", index=False)
logger.info(f"Customers: {customers.shape}")

# Generate transactions
transactions = pd.DataFrame([
    generate_transaction(txn_id, random.randint(1, NUM_CUSTOMERS))
    for txn_id in range(1, NUM_TRANSACTIONS + 1)
])
transactions.to_csv("data/transactions.csv", index=False)
logger.info(f"Transactions: {transactions.shape}")

# Generate attendance
attendance = pd.DataFrame([
    generate_attendance(att_id, random.randint(1, NUM_CUSTOMERS))
    for att_id in range(1, NUM_ATTENDANCES + 1)
])
attendance.to_csv("data/attendance.csv", index=False)
logger.info(f"Attendance: {attendance.shape}")

# -----------------------------------------------------
# Utility to Load Data to DB
# -----------------------------------------------------

def load_csv_to_table(table_name: str, csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    logger.info(f"Data loaded into table: {table_name}")

# -----------------------------------------------------
# Load All CSVs to DB
# -----------------------------------------------------

folder_path = "data/*.csv"
files = glob.glob(folder_path)
base_names = [path.splitext(path.basename(file))[0] for file in files]

for table in base_names:
    try:
        logger.info(f"Loading {table}...")
        load_csv_to_table(table, path.join("data", f"{table}.csv"))
    except Exception as e:
        logger.error(f"Failed to load {table}: {e}")

print("✅ All tables are populated.")
