import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def run_restaurant_analysis():

    conn = get_connection()

    query = """
    SELECT *
    FROM restaurants;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("=" * 50)
    print("RESTAURANT ANALYSIS")
    print("=" * 50)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nAverage Rating:")
    print(round(df["rating"].mean(), 2))

    print("\nCuisine Distribution:")
    print(df["cuisine"].value_counts())

    print("\nRestaurants by City:")
    print(df["city"].value_counts())

    print("\nAverage Preparation Time:")
    print(round(df["avg_preparation_time"].mean(), 2))

    print("\nTop Rated Restaurants:")
    print(
        df.sort_values(
            by="rating",
            ascending=False
        )[["restaurant_name", "rating"]].head(10)
    )