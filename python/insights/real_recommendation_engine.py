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


def generate_real_recommendations():

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

    recommendations = []

    # ==========================================
    # TRAFFIC RECOMMENDATION
    # ==========================================

    jam_orders = df[
        df["traffic_level"] == "Jam"
    ]

    if len(jam_orders) > 0:

        jam_average = jam_orders[
            "actual_delivery_minutes"
        ].mean()

        impact = jam_average - overall_average

        if impact > 3:

            recommendations.append({
                "priority": "High",
                "area": "Traffic",
                "finding": (
                    f"Jam traffic increases delivery time "
                    f"by {impact:.2f} minutes."
                ),
                "recommendation": (
                    "Increase rider availability during "
                    "heavy traffic periods and prioritize "
                    "nearby orders in congested zones."
                )
            })

    # ==========================================
    # PEAK HOUR RECOMMENDATION
    # ==========================================

    peak_orders = df[
        df["peak_hour"] == "Yes"
    ]

    if len(peak_orders) > 0:

        peak_average = peak_orders[
            "actual_delivery_minutes"
        ].mean()

        impact = peak_average - overall_average

        if impact > 2:

            recommendations.append({
                "priority": "High",
                "area": "Peak Hour",
                "finding": (
                    f"Peak-hour deliveries take "
                    f"{impact:.2f} minutes longer on average."
                ),
                "recommendation": (
                    "Deploy additional riders during "
                    "peak hours and dynamically balance "
                    "order assignments."
                )
            })

    # ==========================================
    # MULTIPLE DELIVERY RECOMMENDATION
    # ==========================================

    multi_orders = df[
        df["multiple_deliveries"] >= 2
    ]

    if len(multi_orders) > 0:

        multi_average = multi_orders[
            "actual_delivery_minutes"
        ].mean()

        impact = multi_average - overall_average

        if impact > 8:

            recommendations.append({
                "priority": "Critical",
                "area": "Multiple Deliveries",
                "finding": (
                    f"Multiple-order assignments increase "
                    f"delivery time by {impact:.2f} minutes."
                ),
                "recommendation": (
                    "Limit multi-order assignments during "
                    "high-demand periods and apply stricter "
                    "distance thresholds for order batching."
                )
            })

    # ==========================================
    # VEHICLE CONDITION RECOMMENDATION
    # ==========================================

    poor_vehicle = df[
        df["vehicle_condition"] == 0
    ]

    if len(poor_vehicle) > 0:

        poor_average = poor_vehicle[
            "actual_delivery_minutes"
        ].mean()

        impact = poor_average - overall_average

        if impact > 2:

            recommendations.append({
                "priority": "High",
                "area": "Vehicle Condition",
                "finding": (
                    f"Orders with poor vehicle condition "
                    f"take {impact:.2f} minutes longer."
                ),
                "recommendation": (
                    "Introduce regular vehicle inspections "
                    "and prioritize maintenance for riders "
                    "with poor vehicle-condition scores."
                )
            })

    # ==========================================
    # DISTANCE RECOMMENDATION
    # ==========================================

    long_orders = df[
        df["distance_km"] > 12
    ]

    if len(long_orders) > 0:

        long_average = long_orders[
            "actual_delivery_minutes"
        ].mean()

        impact = long_average - overall_average

        if impact > 2:

            recommendations.append({
                "priority": "Medium",
                "area": "Delivery Distance",
                "finding": (
                    f"Very long-distance orders take "
                    f"{impact:.2f} minutes longer."
                ),
                "recommendation": (
                    "Use distance-aware rider assignment "
                    "and prioritize riders closer to the "
                    "restaurant for long-distance deliveries."
                )
            })

    # ==========================================
    # CITY RECOMMENDATION
    # ==========================================

    city_analysis = (
        df.groupby("city")[
            "actual_delivery_minutes"
        ]
        .agg(["count", "mean"])
        .reset_index()
    )

    city_analysis = city_analysis[
        city_analysis["count"] >= 100
    ]

    if len(city_analysis) > 0:

        worst_city = city_analysis.loc[
            city_analysis["mean"].idxmax()
        ]

        city_impact = (
            worst_city["mean"]
            - overall_average
        )

        if city_impact > 5:

            recommendations.append({
                "priority": "High",
                "area": "City Operations",
                "finding": (
                    f"{worst_city['city']} has an average "
                    f"delivery time of "
                    f"{worst_city['mean']:.2f} minutes."
                ),
                "recommendation": (
                    "Investigate rider availability, traffic "
                    "patterns and delivery-zone allocation "
                    "specifically for this city segment."
                )
            })

    # ==========================================
    # RETURN
    # ==========================================

    return recommendations


if __name__ == "__main__":

    recommendations = generate_real_recommendations()

    print("=" * 70)
    print("OPSLENS AI - REAL DATA RECOMMENDATION ENGINE")
    print("=" * 70)

    print(
        f"\nTotal recommendations generated: "
        f"{len(recommendations)}"
    )

    for i, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"Recommendation #{i}"
        )

        print(
            f"Priority: "
            f"{recommendation['priority']}"
        )

        print(
            f"Area: "
            f"{recommendation['area']}"
        )

        print(
            f"Finding: "
            f"{recommendation['finding']}"
        )

        print(
            f"Action: "
            f"{recommendation['recommendation']}"
        )

    print("\n" + "=" * 70)
    print(
        "Real recommendation engine completed successfully!"
    )
    print("=" * 70)