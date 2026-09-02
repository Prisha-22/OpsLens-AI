import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def run_order_analysis():

    conn = get_connection()

    query = """
    SELECT *
    FROM orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("=" * 50)
    print("ORDER ANALYSIS")
    print("=" * 50)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nTotal Revenue:")
    print(round(df["order_value"].sum(), 2))

    print("\nAverage Order Value:")
    print(round(df["order_value"].mean(), 2))

    print("\nAverage Delivery Time:")
    print(round(df["actual_delivery_minutes"].mean(), 2))

    print("\nDelivery Status:")
    print(df["delivery_status"].value_counts())

    print("\nWeather Conditions:")
    print(df["weather"].value_counts())

    print("\nTraffic Levels:")
    print(df["traffic_level"].value_counts())

    print("\nTop 10 Highest Value Orders:")
    print(
        df.sort_values(
            by="order_value",
            ascending=False
        )[["order_id", "order_value"]].head(10)
    )