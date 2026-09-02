import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(PROJECT_ROOT)

import pandas as pd

from python.database import get_connection


def analyze_real_root_causes():

    conn = get_connection()

    query = """
    SELECT
        order_id,
        distance_km,
        weather,
        traffic_level,
        peak_hour,
        weekend,
        order_type,
        vehicle_type,
        vehicle_condition,
        multiple_deliveries,
        city,
        actual_delivery_minutes
    FROM real_delivery_orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==========================================
    # OVERALL BASELINE
    # ==========================================

    overall_average = df[
        "actual_delivery_minutes"
    ].mean()

    # ==========================================
    # HELPER FUNCTION
    # ==========================================

    def factor_analysis(column):

        result = (
            df.groupby(column, dropna=False)[
                "actual_delivery_minutes"
            ]
            .agg(
                order_count="count",
                average_delivery_time="mean",
                median_delivery_time="median"
            )
            .reset_index()
        )

        # Standardize factor column name for Insight Engine
        result = result.rename(
            columns={column: "factor"}
        )

        result = result.sort_values(
            "average_delivery_time",
            ascending=False
        )

        result["impact_vs_average"] = (
            result["average_delivery_time"]
            - overall_average
        )

        return result.round(2)

    # ==========================================
    # TRAFFIC
    # ==========================================

    traffic = factor_analysis(
        "traffic_level"
    )

    # ==========================================
    # WEATHER
    # ==========================================

    weather = factor_analysis(
        "weather"
    )

    # ==========================================
    # PEAK HOUR
    # ==========================================

    peak = factor_analysis(
        "peak_hour"
    )

    # ==========================================
    # WEEKEND
    # ==========================================

    weekend = factor_analysis(
        "weekend"
    )

    # ==========================================
    # ORDER TYPE
    # ==========================================

    order_type = factor_analysis(
        "order_type"
    )

    # ==========================================
    # VEHICLE TYPE
    # ==========================================

    vehicle_type = factor_analysis(
        "vehicle_type"
    )

    # ==========================================
    # VEHICLE CONDITION
    # ==========================================

    vehicle_condition = factor_analysis(
        "vehicle_condition"
    )

    # ==========================================
    # MULTIPLE DELIVERIES
    # ==========================================

    multiple_deliveries = factor_analysis(
        "multiple_deliveries"
    )

    # ==========================================
    # CITY
    # ==========================================

    city = factor_analysis(
        "city"
    )

    # ==========================================
    # DISTANCE CATEGORY
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

    distance = factor_analysis(
        "distance_category"
    )

    return {
        "overall_average": overall_average,
        "traffic": traffic,
        "weather": weather,
        "peak": peak,
        "weekend": weekend,
        "order_type": order_type,
        "vehicle_type": vehicle_type,
        "vehicle_condition": vehicle_condition,
        "multiple_deliveries": multiple_deliveries,
        "city": city,
        "distance": distance
    }


if __name__ == "__main__":

    results = analyze_real_root_causes()

    print("=" * 65)
    print("OPSLENS AI - REAL DATA ROOT CAUSE ANALYSIS")
    print("=" * 65)

    print(
        f"\nOverall Average Delivery Time: "
        f"{results['overall_average']:.2f} minutes"
    )

    print("\nTraffic:")
    print(
        results["traffic"]
        .to_string(index=False)
    )

    print("\nWeather:")
    print(
        results["weather"]
        .to_string(index=False)
    )

    print("\nPeak Hour:")
    print(
        results["peak"]
        .to_string(index=False)
    )

    print("\nWeekend:")
    print(
        results["weekend"]
        .to_string(index=False)
    )

    print("\nOrder Type:")
    print(
        results["order_type"]
        .to_string(index=False)
    )

    print("\nVehicle Type:")
    print(
        results["vehicle_type"]
        .to_string(index=False)
    )

    print("\nVehicle Condition:")
    print(
        results["vehicle_condition"]
        .to_string(index=False)
    )

    print("\nMultiple Deliveries:")
    print(
        results["multiple_deliveries"]
        .to_string(index=False)
    )

    print("\nCity:")
    print(
        results["city"]
        .head(15)
        .to_string(index=False)
    )

    print("\nDistance:")
    print(
        results["distance"]
        .to_string(index=False)
    )

    print(
        "\nReal root cause analysis completed successfully!"
    )