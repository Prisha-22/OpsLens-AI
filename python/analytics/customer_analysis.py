import os
import sys

# Add parent directory (python/) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def run_customer_analysis():

    # Connect to PostgreSQL
    conn = get_connection()

    # Read customer data
    query = """
    SELECT *
    FROM customers;
    """

    df = pd.read_sql(query, conn)

    # Close connection
    conn.close()

    # -------------------------------
    # Basic Dataset Information
    # -------------------------------
    print("=" * 50)
    print("CUSTOMER ANALYSIS")
    print("=" * 50)

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nMembership Distribution:")
    print(df["membership"].value_counts())

    print("\nCustomers by City:")
    print(df["city"].value_counts())

    print("\nAverage Orders Per Customer:")
    print(round(df["total_orders"].mean(), 2))

    print("\nTop 10 Customers:")
    top_customers = df.sort_values(by="total_orders", ascending=False)
    print(top_customers[["customer_name", "total_orders"]].head(10))