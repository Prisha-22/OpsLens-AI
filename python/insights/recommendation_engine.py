import os
import sys

# Add project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

# Add python folder
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import pandas as pd

from database import get_connection


def generate_recommendations():

    # ==========================================
    # LOAD ORDER DATA
    # ==========================================

    conn = get_connection()

    query = """
    SELECT
        order_id,
        distance_km,
        order_value,
        actual_delivery_minutes,
        weather,
        traffic_level,
        peak_hour,
        weekend,
        delivery_status
    FROM orders;
    """

    orders = pd.read_sql(query, conn)

    conn.close()

    recommendations = []

    # ==========================================
    # OVERALL METRICS
    # ==========================================

    total_orders = len(orders)

    delayed_orders = len(
        orders[
            orders["delivery_status"] == "Delayed"
        ]
    )

    cancelled_orders = len(
        orders[
            orders["delivery_status"] == "Cancelled"
        ]
    )

    delay_rate = (
        delayed_orders / total_orders
    ) * 100

    cancellation_rate = (
        cancelled_orders / total_orders
    ) * 100

    # ==========================================
    # 1. DELIVERY DELAY RECOMMENDATION
    # ==========================================

    if delay_rate >= 10:

        recommendations.append({
            "priority": "High",
            "category": "Delivery Delays",
            "issue": (
                f"{delay_rate:.1f}% of orders are delayed."
            ),
            "recommendation": (
                "Increase rider availability, investigate "
                "high-delay zones and optimize peak-hour "
                "delivery capacity."
            ),
            "action": (
                "Review delayed orders by city, traffic "
                "level and peak-hour status."
            )
        })

    elif delay_rate >= 5:

        recommendations.append({
            "priority": "Medium",
            "category": "Delivery Delays",
            "issue": (
                f"{delay_rate:.1f}% of orders are delayed."
            ),
            "recommendation": (
                "Monitor recurring delivery delays and "
                "identify operational patterns."
            ),
            "action": (
                "Track delayed orders by traffic, weather "
                "and delivery zone."
            )
        })

    else:

        recommendations.append({
            "priority": "Low",
            "category": "Delivery Delays",
            "issue": (
                f"Only {delay_rate:.1f}% of orders are delayed."
            ),
            "recommendation": (
                "Maintain current delivery operations."
            ),
            "action": (
                "Continue monitoring delay trends."
            )
        })

    # ==========================================
    # 2. TRAFFIC RECOMMENDATION
    # ==========================================

    traffic = (
        orders
        .groupby("traffic_level")[
            "actual_delivery_minutes"
        ]
        .mean()
        .sort_values(ascending=False)
    )

    worst_traffic = traffic.index[0]
    worst_traffic_time = traffic.iloc[0]

    overall_delivery = orders[
        "actual_delivery_minutes"
    ].mean()

    traffic_impact = (
        worst_traffic_time - overall_delivery
    )

    if traffic_impact > 0.5:

        recommendations.append({
            "priority": "High",
            "category": "Traffic",
            "issue": (
                f"{worst_traffic} traffic has the highest "
                f"average delivery time "
                f"({worst_traffic_time:.1f} min)."
            ),
            "recommendation": (
                "Increase rider allocation and monitor "
                "high-traffic zones during busy periods."
            ),
            "action": (
                f"Prioritize operational capacity in "
                f"{worst_traffic.lower()} traffic conditions."
            )
        })

    # ==========================================
    # 3. WEATHER RECOMMENDATION
    # ==========================================

    weather = (
        orders
        .groupby("weather")[
            "actual_delivery_minutes"
        ]
        .mean()
        .sort_values(ascending=False)
    )

    worst_weather = weather.index[0]
    worst_weather_time = weather.iloc[0]

    weather_impact = (
        worst_weather_time - overall_delivery
    )

    if weather_impact > 0.5:

        recommendations.append({
            "priority": "Medium",
            "category": "Weather",
            "issue": (
                f"{worst_weather} weather has the highest "
                f"average delivery time "
                f"({worst_weather_time:.1f} min)."
            ),
            "recommendation": (
                "Prepare additional rider capacity and "
                "monitor delivery performance during "
                "adverse weather."
            ),
            "action": (
                f"Activate weather monitoring when "
                f"{worst_weather.lower()} conditions occur."
            )
        })

    # ==========================================
    # 4. PEAK HOUR RECOMMENDATION
    # ==========================================

    peak = (
        orders
        .groupby("peak_hour")[
            "actual_delivery_minutes"
        ]
        .mean()
    )

    if "Yes" in peak.index and "No" in peak.index:

        peak_impact = (
            peak["Yes"] - peak["No"]
        )

        if peak_impact > 0.5:

            recommendations.append({
                "priority": "High",
                "category": "Peak Hour",
                "issue": (
                    f"Peak-hour deliveries take "
                    f"{peak_impact:+.2f} minutes longer."
                ),
                "recommendation": (
                    "Optimize rider allocation and increase "
                    "operational capacity during peak hours."
                ),
                "action": (
                    "Schedule additional riders before "
                    "peak-hour demand begins."
                )
            })

    # ==========================================
    # 5. CANCELLATION RECOMMENDATION
    # ==========================================

    if cancellation_rate >= 5:

        recommendations.append({
            "priority": "High",
            "category": "Cancellations",
            "issue": (
                f"{cancellation_rate:.1f}% of orders "
                f"were cancelled."
            ),
            "recommendation": (
                "Investigate cancellation reasons and "
                "identify operational factors causing "
                "order failures."
            ),
            "action": (
                "Analyze cancellations by traffic, "
                "weather, restaurant and delivery status."
            )
        })

    elif cancellation_rate >= 3:

        recommendations.append({
            "priority": "Medium",
            "category": "Cancellations",
            "issue": (
                f"{cancellation_rate:.1f}% of orders "
                f"were cancelled."
            ),
            "recommendation": (
                "Monitor cancellation patterns and "
                "investigate recurring causes."
            ),
            "action": (
                "Review cancellation trends by "
                "operational conditions."
            )
        })

    # ==========================================
    # 6. DISTANCE RECOMMENDATION
    # ==========================================

    long_distance = orders[
        orders["distance_km"] > 12
    ]

    long_distance_rate = (
        len(long_distance) / total_orders
    ) * 100

    if long_distance_rate >= 10:

        recommendations.append({
            "priority": "Medium",
            "category": "Long-Distance Orders",
            "issue": (
                f"{long_distance_rate:.1f}% of orders "
                f"are longer than 12 km."
            ),
            "recommendation": (
                "Review long-distance delivery zones "
                "and optimize rider allocation."
            ),
            "action": (
                "Monitor delivery time and cancellation "
                "rates for long-distance orders."
            )
        })

    # ==========================================
    # RETURN
    # ==========================================

    return recommendations


if __name__ == "__main__":

    results = generate_recommendations()

    print("=" * 60)
    print("OPSLENS AI - OPERATIONAL RECOMMENDATION ENGINE")
    print("=" * 60)

    for i, item in enumerate(results, start=1):

        print(
            f"\n{i}. [{item['priority']}] "
            f"{item['category']}"
        )

        print(
            f"Issue: {item['issue']}"
        )

        print(
            f"Recommendation: "
            f"{item['recommendation']}"
        )

        print(
            f"Action: "
            f"{item['action']}"
        )

    print("\n" + "=" * 60)
    print("Recommendation generation completed successfully!")
    print("=" * 60)