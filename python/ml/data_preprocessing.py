import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def load_data():

    conn = get_connection()

    query = """
    SELECT
        distance_km,
        weather,
        traffic_level,
        peak_hour,
        weekend,
        order_type,
        delivery_fee,
        discount,
        actual_delivery_minutes
    FROM orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("=" * 50)
    print("DATA PREPROCESSING")
    print("=" * 50)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nMissing Values:")
    print(df.isnull().sum())

    return df


if __name__ == "__main__":
    load_data()