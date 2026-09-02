import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def run_rider_analysis():

    conn = get_connection()

    query = """
    SELECT *
    FROM riders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("=" * 50)
    print("RIDER ANALYSIS")
    print("=" * 50)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nAverage Rider Rating:")
    print(round(df["rating"].mean(), 2))

    print("\nVehicle Types:")
    print(df["vehicle_type"].value_counts())

    print("\nCities:")
    print(df["city"].value_counts())

    print("\nTop Rated Riders:")
    print(
        df.sort_values(
            by="rating",
            ascending=False
        )[["rider_name", "rating"]].head(10)
    )

    print("\nJoining Date Summary:")
    print(df["joining_date"].describe())