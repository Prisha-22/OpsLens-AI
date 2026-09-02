import os
import sys

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

# Add python folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import pandas as pd

from database import get_connection


def analyze_root_causes():

    conn = get_connection()

    query = """
    SELECT
        order_id,
        order_time,
        distance_km,
        weather,
        traffic_level,
        peak_hour,
        weekend,
        order_type,
        actual_delivery_minutes,
        delivery_status
    FROM orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==========================================
    # Overall baseline
    # ==========================================

    overall_average = df[
        "actual_delivery_minutes"
    ].mean()

    # ==========================================
    # Traffic Analysis
    # ==========================================

    traffic = (
        df.groupby("traffic_level")[
            "actual_delivery_minutes"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "actual_delivery_minutes",
            ascending=False
        )
    )

    traffic.columns = [
        "factor",
        "average_delivery_time"
    ]

    traffic["impact"] = (
        traffic["average_delivery_time"]
        - overall_average
    )

    # ==========================================
    # Weather Analysis
    # ==========================================

    weather = (
        df.groupby("weather")[
            "actual_delivery_minutes"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "actual_delivery_minutes",
            ascending=False
        )
    )

    weather.columns = [
        "factor",
        "average_delivery_time"
    ]

    weather["impact"] = (
        weather["average_delivery_time"]
        - overall_average
    )

    # ==========================================
    # Peak Hour Analysis
    # ==========================================

    peak = (
        df.groupby("peak_hour")[
            "actual_delivery_minutes"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "actual_delivery_minutes",
            ascending=False
        )
    )

    peak.columns = [
        "factor",
        "average_delivery_time"
    ]

    peak["impact"] = (
        peak["average_delivery_time"]
        - overall_average
    )

    # ==========================================
    # Weekend Analysis
    # ==========================================

    weekend = (
        df.groupby("weekend")[
            "actual_delivery_minutes"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "actual_delivery_minutes",
            ascending=False
        )
    )

    weekend.columns = [
        "factor",
        "average_delivery_time"
    ]

    weekend["impact"] = (
        weekend["average_delivery_time"]
        - overall_average
    )

    # ==========================================
    # Order Type Analysis
    # ==========================================

    order_type = (
        df.groupby("order_type")[
            "actual_delivery_minutes"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "actual_delivery_minutes",
            ascending=False
        )
    )

    order_type.columns = [
        "factor",
        "average_delivery_time"
    ]

    order_type["impact"] = (
        order_type["average_delivery_time"]
        - overall_average
    )

    # ==========================================
    # Distance Analysis
    # ==========================================

    df["distance_category"] = pd.cut(
        df["distance_km"],
        bins=[
            0,
            3,
            7,
            12,
            float("inf")
        ],
        labels=[
            "Short (0-3 km)",
            "Medium (3-7 km)",
            "Long (7-12 km)",
            "Very Long (12+ km)"
        ]
    )

    distance = (
        df.groupby(
            "distance_category",
            observed=True
        )[
            "actual_delivery_minutes"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "actual_delivery_minutes",
            ascending=False
        )
    )

    distance.columns = [
        "factor",
        "average_delivery_time"
    ]

    distance["impact"] = (
        distance["average_delivery_time"]
        - overall_average
    )

    # ==========================================
    # Return Results
    # ==========================================

    return {
        "overall_average": overall_average,
        "traffic": traffic,
        "weather": weather,
        "peak": peak,
        "weekend": weekend,
        "order_type": order_type,
        "distance": distance
    }


if __name__ == "__main__":

    results = analyze_root_causes()

    print("=" * 60)
    print("OPSLENS AI - ROOT CAUSE ANALYSIS")
    print("=" * 60)

    print(
        f"\nOverall Average Delivery Time: "
        f"{results['overall_average']:.2f} minutes"
    )

    print("\n🚦 Traffic:")
    print(results["traffic"].to_string(index=False))

    print("\n🌦 Weather:")
    print(results["weather"].to_string(index=False))

    print("\n⏰ Peak Hour:")
    print(results["peak"].to_string(index=False))

    print("\n📍 Distance:")
    print(results["distance"].to_string(index=False))

    print("\n📦 Order Type:")
    print(results["order_type"].to_string(index=False))

    print("\n📅 Weekend:")
    print(results["weekend"].to_string(index=False))

    print("\nRoot cause analysis completed successfully!")