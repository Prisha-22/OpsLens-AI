import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)

import pandas as pd

from python.database import get_connection

def run_real_delivery_analysis():

    conn = get_connection()

    query = """
    SELECT *
    FROM real_delivery_orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    print("=" * 60)
    print("REAL ZOMATO DELIVERY ANALYSIS")
    print("=" * 60)

    # ==========================================
    # DATASET OVERVIEW
    # ==========================================

    print("\nDataset Shape:")
    print(df.shape)

    print("\nTotal Orders:")
    print(len(df))

    # ==========================================
    # DELIVERY PERFORMANCE
    # ==========================================

    print("\nAverage Delivery Time:")
    print(
        round(
            df["actual_delivery_minutes"].mean(),
            2
        )
    )

    print("\nMinimum Delivery Time:")
    print(
        df["actual_delivery_minutes"].min()
    )

    print("\nMaximum Delivery Time:")
    print(
        df["actual_delivery_minutes"].max()
    )

    # ==========================================
    # DISTANCE
    # ==========================================

    print("\nAverage Delivery Distance:")
    print(
        round(
            df["distance_km"].mean(),
            2
        )
    )

    print("\nMaximum Delivery Distance:")
    print(
        df["distance_km"].max()
    )

    # ==========================================
    # TRAFFIC
    # ==========================================

    print("\nDelivery Time by Traffic Level:")

    traffic_analysis = (
        df.groupby("traffic_level")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean", "median"]
        )
        .round(2)
        .sort_values(
            by="mean",
            ascending=False
        )
    )

    print(traffic_analysis)

    # ==========================================
    # WEATHER
    # ==========================================

    print("\nDelivery Time by Weather:")

    weather_analysis = (
        df.groupby("weather")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean", "median"]
        )
        .round(2)
        .sort_values(
            by="mean",
            ascending=False
        )
    )

    print(weather_analysis)

    # ==========================================
    # PEAK HOUR
    # ==========================================

    print("\nPeak Hour Impact:")

    peak_analysis = (
        df.groupby("peak_hour")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean", "median"]
        )
        .round(2)
    )

    print(peak_analysis)

    # ==========================================
    # WEEKEND
    # ==========================================

    print("\nWeekend vs Weekday:")

    weekend_analysis = (
        df.groupby("weekend")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean", "median"]
        )
        .round(2)
    )

    print(weekend_analysis)

    # ==========================================
    # CITY PERFORMANCE
    # ==========================================

    print("\nTop 10 Cities by Average Delivery Time:")

    city_analysis = (
        df.groupby("city")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean"]
        )
        .round(2)
        .sort_values(
            by="mean",
            ascending=False
        )
        .head(10)
    )

    print(city_analysis)

    # ==========================================
    # DISTANCE vs DELIVERY TIME
    # ==========================================

    print("\nDistance vs Delivery Time Correlation:")

    correlation = df[
        [
            "distance_km",
            "actual_delivery_minutes"
        ]
    ].corr().iloc[0, 1]

    print(round(correlation, 3))

    # ==========================================
    # MULTIPLE DELIVERIES
    # ==========================================

    print("\nMultiple Deliveries Impact:")

    multiple_delivery_analysis = (
        df.groupby("multiple_deliveries")
        ["actual_delivery_minutes"]
        .agg(
            ["count", "mean", "median"]
        )
        .round(2)
        .sort_values(
            by="mean",
            ascending=False
        )
    )

    print(multiple_delivery_analysis)

    # ==========================================
    # RIDER RATING
    # ==========================================

    print("\nAverage Delivery Time by Rider Rating:")

    rider_rating_analysis = (
        df.groupby("rider_rating")
        ["actual_delivery_minutes"]
        .mean()
        .round(2)
        .sort_index()
    )

    print(rider_rating_analysis)

    print(
        "\nReal delivery analysis completed successfully!"
    )


if __name__ == "__main__":

    run_real_delivery_analysis()