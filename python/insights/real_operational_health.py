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


def calculate_operational_health():

    conn = get_connection()

    query = """
    SELECT
        actual_delivery_minutes,
        traffic_level,
        peak_hour,
        vehicle_condition,
        multiple_deliveries,
        distance_km,
        city
    FROM real_delivery_orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==========================================
    # BASELINE
    # ==========================================

    overall_average = df[
        "actual_delivery_minutes"
    ].mean()

    # ==========================================
    # OPERATIONAL INDICATORS
    # ==========================================

    jam_delivery_time = df.loc[
        df["traffic_level"] == "Jam",
        "actual_delivery_minutes"
    ].mean()

    peak_delivery_time = df.loc[
        df["peak_hour"] == "Yes",
        "actual_delivery_minutes"
    ].mean()

    multi_delivery_time = df.loc[
        df["multiple_deliveries"] >= 2,
        "actual_delivery_minutes"
    ].mean()

    poor_vehicle_time = df.loc[
        df["vehicle_condition"] == 0,
        "actual_delivery_minutes"
    ].mean()

    very_long_distance_time = df.loc[
        df["distance_km"] > 12,
        "actual_delivery_minutes"
    ].mean()

    # ==========================================
    # OPERATIONAL RISK RATES
    # ==========================================

    jam_rate = (
        (df["traffic_level"] == "Jam").mean()
        * 100
    )

    peak_rate = (
        (df["peak_hour"] == "Yes").mean()
        * 100
    )

    multi_delivery_rate = (
        (df["multiple_deliveries"] >= 2).mean()
        * 100
    )

    poor_vehicle_rate = (
        (df["vehicle_condition"] == 0).mean()
        * 100
    )

    very_long_distance_rate = (
        (df["distance_km"] > 12).mean()
        * 100
    )

    # ==========================================
    # HEALTH SCORE
    # ==========================================

    score = 100

    if jam_rate > 35:
        score -= 15
    elif jam_rate > 25:
        score -= 10
    elif jam_rate > 15:
        score -= 5

    if peak_rate > 60:
        score -= 15
    elif peak_rate > 50:
        score -= 10
    elif peak_rate > 40:
        score -= 5

    if multi_delivery_rate > 8:
        score -= 20
    elif multi_delivery_rate > 5:
        score -= 15
    elif multi_delivery_rate > 3:
        score -= 10

    if poor_vehicle_rate > 10:
        score -= 15
    elif poor_vehicle_rate > 5:
        score -= 10
    elif poor_vehicle_rate > 2:
        score -= 5

    if very_long_distance_rate > 40:
        score -= 15
    elif very_long_distance_rate > 30:
        score -= 10
    elif very_long_distance_rate > 20:
        score -= 5

    score = max(0, min(100, score))

    # ==========================================
    # HEALTH STATUS
    # ==========================================

    if score >= 80:
        status = "Healthy"
    elif score >= 60:
        status = "Moderate Risk"
    elif score >= 40:
        status = "High Risk"
    else:
        status = "Critical"

    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return {
        "health_score": score,
        "status": status,
        "overall_average_delivery_time": overall_average,
        "jam_delivery_time": jam_delivery_time,
        "peak_delivery_time": peak_delivery_time,
        "multiple_delivery_time": multi_delivery_time,
        "poor_vehicle_delivery_time": poor_vehicle_time,
        "very_long_distance_delivery_time": very_long_distance_time,
        "jam_rate": jam_rate,
        "peak_rate": peak_rate,
        "multiple_delivery_rate": multi_delivery_rate,
        "poor_vehicle_rate": poor_vehicle_rate,
        "very_long_distance_rate": very_long_distance_rate
    }


if __name__ == "__main__":

    result = calculate_operational_health()

    print("=" * 65)
    print("OPSLENS AI - REAL DATA OPERATIONAL HEALTH")
    print("=" * 65)

    print(
        f"\nOperational Health Score: "
        f"{result['health_score']}/100"
    )

    print(
        f"Operational Status: "
        f"{result['status']}"
    )

    print(
        f"\nAverage Delivery Time: "
        f"{result['overall_average_delivery_time']:.2f} minutes"
    )

    print("\nOperational Indicators:")

    print(
        f"Jam Traffic Rate: "
        f"{result['jam_rate']:.2f}%"
    )

    print(
        f"Peak Hour Rate: "
        f"{result['peak_rate']:.2f}%"
    )

    print(
        f"Multiple Delivery Rate: "
        f"{result['multiple_delivery_rate']:.2f}%"
    )

    print(
        f"Poor Vehicle Condition Rate: "
        f"{result['poor_vehicle_rate']:.2f}%"
    )

    print(
        f"Very Long Distance Rate: "
        f"{result['very_long_distance_rate']:.2f}%"
    )

    print(
        "\nReal operational health analysis completed successfully!"
    )