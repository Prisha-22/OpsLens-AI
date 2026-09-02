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
from ml.anomaly_detection import detect_anomalies
from ml.forecast import generate_forecast
from python.ml.real_anomaly_detection import detect_real_anomalies
from python.analytics.real_root_cause_analysis import analyze_real_root_causes
from python.insights.real_operational_health import calculate_operational_health
from python.insights.real_recommendation_engine import generate_real_recommendations

def generate_insights():

    # ==========================================
    # LOAD ORDERS
    # ==========================================

    conn = get_connection()

    query = """
    SELECT
        order_id,
        order_time,
        distance_km,
        order_value,
        delivery_fee,
        discount,
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

    insights = []

    # ==========================================
    # OVERALL PERFORMANCE
    # ==========================================

    average_delivery = orders[
        "actual_delivery_minutes"
    ].mean()

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

    delayed_percentage = (
        delayed_orders / total_orders
    ) * 100

    cancelled_percentage = (
        cancelled_orders / total_orders
    ) * 100

    # ==========================================
    # DELIVERY TIME INSIGHT
    # ==========================================

    insights.append({
        "category": "Performance",
        "severity": "Info",
        "insight": (
            f"Average delivery time is "
            f"{average_delivery:.1f} minutes across "
            f"{total_orders:,} orders."
        ),
        "recommendation": (
            "Monitor delivery-time trends and identify "
            "operational factors contributing to delays."
        )
    })

    # ==========================================
    # DELAY INSIGHT
    # ==========================================

    if delayed_percentage >= 10:

        severity = "High"

        recommendation = (
            "Investigate traffic, rider availability, "
            "weather and peak-hour operations."
        )

    elif delayed_percentage >= 5:

        severity = "Medium"

        recommendation = (
            "Monitor delayed orders and identify "
            "recurring operational patterns."
        )

    else:

        severity = "Info"

        recommendation = (
            "Current delay levels appear relatively controlled."
        )

    insights.append({
        "category": "Delivery Delays",
        "severity": severity,
        "insight": (
            f"{delayed_orders:,} orders "
            f"({delayed_percentage:.1f}%) "
            f"were marked as delayed."
        ),
        "recommendation": recommendation
    })

    # ==========================================
    # CANCELLATION INSIGHT
    # ==========================================

    insights.append({
        "category": "Cancellations",
        "severity": (
            "High"
            if cancelled_percentage >= 5
            else "Medium"
        ),
        "insight": (
            f"{cancelled_orders:,} orders "
            f"({cancelled_percentage:.1f}%) "
            f"were cancelled."
        ),
        "recommendation": (
            "Analyze cancellation reasons and identify "
            "patterns related to traffic, weather and "
            "delivery conditions."
        )
    })

    # ==========================================
    # TRAFFIC ANALYSIS
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

    insights.append({
        "category": "Traffic",
        "severity": "High",
        "insight": (
            f"{worst_traffic} traffic has the highest "
            f"average delivery time at "
            f"{worst_traffic_time:.1f} minutes."
        ),
        "recommendation": (
            f"Consider increasing rider availability "
            f"and monitoring {worst_traffic.lower()}-traffic "
            f"zones during busy periods."
        )
    })

    # ==========================================
    # WEATHER ANALYSIS
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

    insights.append({
        "category": "Weather",
        "severity": "Medium",
        "insight": (
            f"{worst_weather} weather is associated with "
            f"the highest average delivery time of "
            f"{worst_weather_time:.1f} minutes."
        ),
        "recommendation": (
            "Prepare additional operational capacity "
            "during adverse weather conditions."
        )
    })

    # ==========================================
    # PEAK HOUR ANALYSIS
    # ==========================================

    peak = (
        orders
        .groupby("peak_hour")[
            "actual_delivery_minutes"
        ]
        .mean()
    )

    if "Yes" in peak.index and "No" in peak.index:

        difference = (
            peak["Yes"] - peak["No"]
        )

        insights.append({
            "category": "Peak Hour",
            "severity": (
                "High"
                if difference > 3
                else "Medium"
            ),
            "insight": (
                f"Peak-hour deliveries take "
                f"{difference:+.1f} minutes compared "
                f"with non-peak periods."
            ),
            "recommendation": (
                "Optimize rider allocation and "
                "operational capacity during peak hours."
            )
        })
    # ==========================================
    # ANOMALY DETECTION
    # ==========================================

    try:

        anomalies = detect_anomalies()

        anomaly_count = len(anomalies)

        anomaly_percentage = (
            anomaly_count / total_orders
        ) * 100

        if anomaly_percentage >= 5:

            anomaly_severity = "High"

            anomaly_recommendation = (
                "Investigate anomalous orders immediately "
                "to identify unusual delivery distances, "
                "delivery times, pricing patterns or "
                "operational failures."
            )

        elif anomaly_percentage >= 2:

            anomaly_severity = "Medium"

            anomaly_recommendation = (
                "Monitor anomalous orders and investigate "
                "repeated operational patterns."
            )

        else:

            anomaly_severity = "Info"

            anomaly_recommendation = (
                "Anomaly levels are currently relatively low."
            )

        insights.append({
            "category": "Anomaly Detection",
            "severity": anomaly_severity,
            "insight": (
                f"{anomaly_count:,} orders "
                f"({anomaly_percentage:.1f}%) "
                f"were identified as operational anomalies."
            ),
            "recommendation": anomaly_recommendation
        })

    except Exception as e:

        print(
            f"Anomaly analysis unavailable: {e}"
        )

    # ==========================================
    # DELIVERY FORECAST
    # ==========================================

    try:

        historical, forecast = generate_forecast()

        current_average = (
            historical["average_delivery_time"].iloc[-1]
        )

        forecast_average = (
            forecast["predicted_delivery_time"].mean()
        )

        forecast_change = (
            forecast_average - average_delivery
        )

        if forecast_change >= 3:

            forecast_severity = "High"

            forecast_recommendation = (
                "Prepare additional operational capacity "
                "because delivery times are expected to increase."
            )

        elif forecast_change >= 1:

            forecast_severity = "Medium"

            forecast_recommendation = (
                "Monitor upcoming delivery-time trends "
                "and prepare for a possible increase."
            )

        elif forecast_change <= -3:

            forecast_severity = "Info"

            forecast_recommendation = (
                "Forecast indicates improving delivery "
                "performance. Continue monitoring the trend."
            )

        else:

            forecast_severity = "Info"

            forecast_recommendation = (
                "Delivery performance is expected to remain "
                "relatively stable."
            )

        insights.append({
            "category": "Delivery Forecast",
            "severity": forecast_severity,
            "insight": (
                f"7-day forecast predicts an average delivery "
                f"time of {forecast_average:.1f} minutes, "
                f"representing a {forecast_change:+.1f} minute "
                f"change compared with the current average."
            ),
            "recommendation": forecast_recommendation
        })

    except Exception as e:

        print(
            f"Forecast analysis unavailable: {e}"
        )
    # ==========================================
    # HIGH-VALUE ORDERS
    # ==========================================

    high_value_threshold = orders[
        "order_value"
    ].quantile(0.95)

    high_value_orders = orders[
        orders["order_value"] >= high_value_threshold
    ]

    insights.append({
        "category": "Revenue",
        "severity": "Info",
        "insight": (
            f"The top 5% of orders have values above "
            f"₹{high_value_threshold:,.2f}."
        ),
        "recommendation": (
            "Monitor high-value orders closely because "
            "delivery failures or cancellations may have "
            "greater financial impact."
        )
    })

    # ==========================================
    # RETURN
    # ==========================================

    return insights

    # ==========================================
# REAL DATA AI INSIGHTS
# ==========================================

def generate_real_insights():

    insights = []

    # ==========================================
    # OPERATIONAL HEALTH
    # ==========================================

    try:

        health = calculate_operational_health()

        health_score = health["health_score"]
        status = health["status"]

        insights.append({
            "category": "Operational Health",
            "severity": (
                "Critical"
                if health_score < 40
                else "High"
                if health_score < 60
                else "Medium"
                if health_score < 80
                else "Info"
            ),
            "insight": (
                f"Real delivery operations have a "
                f"health score of {health_score}/100 "
                f"with an overall status of {status}."
            ),
            "recommendation": (
                "Prioritize the operational factors with "
                "the highest delivery-time impact."
            )
        })

    except Exception as e:

        print(
            f"Real operational health unavailable: {e}"
        )

    # ==========================================
    # ROOT CAUSE ANALYSIS
    # ==========================================

    try:

        root_causes = analyze_real_root_causes()

        traffic = root_causes["traffic"]

        worst_traffic = traffic.iloc[0]

        insights.append({
            "category": "Real Root Cause",
            "severity": "High",
            "insight": (
                f"{worst_traffic['factor']} traffic is the "
                f"largest traffic-related contributor, "
                f"with average delivery time of "
                f"{worst_traffic['average_delivery_time']:.1f} "
                f"minutes."
            ),
            "recommendation": (
                "Increase rider availability and optimize "
                "order assignment during congested periods."
            )
        })

        multiple = root_causes["multiple_deliveries"]

        worst_multiple = multiple.iloc[0]

        insights.append({
            "category": "Order Batching",
            "severity": "Critical",
            "insight": (
                f"Orders with {worst_multiple['factor']} "
                f"multiple deliveries average "
                f"{worst_multiple['average_delivery_time']:.1f} "
                f"minutes."
            ),
            "recommendation": (
                "Apply stricter batching and distance "
                "thresholds for multiple-order assignments."
            )
        })

    except Exception as e:

        print(
            f"Real root cause analysis unavailable: {e}"
        )

    # ==========================================
    # REAL ANOMALIES
    # ==========================================

    try:

        anomalies = detect_real_anomalies()

        anomaly_count = len(anomalies)

        insights.append({
            "category": "Real Anomalies",
            "severity": "High",
            "insight": (
                f"{anomaly_count:,} operational anomalies "
                f"were detected in the real delivery dataset."
            ),
            "recommendation": (
                "Investigate unusual combinations of "
                "delivery time, distance, vehicle condition "
                "and multiple deliveries."
            )
        })

    except Exception as e:

        print(
            f"Real anomaly analysis unavailable: {e}"
        )

    # ==========================================
    # REAL RECOMMENDATIONS
    # ==========================================

    try:

        recommendations = generate_real_recommendations()

        critical_count = sum(
            1
            for r in recommendations
            if r.get("priority") == "Critical"
        )

        high_count = sum(
            1
            for r in recommendations
            if r.get("priority") == "High"
        )

        insights.append({
            "category": "AI Recommendations",
            "severity": (
                "Critical"
                if critical_count > 0
                else "High"
                if high_count > 0
                else "Medium"
            ),
            "insight": (
                f"The recommendation engine generated "
                f"{len(recommendations)} operational "
                f"recommendations, including "
                f"{critical_count} critical and "
                f"{high_count} high-priority actions."
            ),
            "recommendation": (
                "Prioritize critical actions first, "
                "followed by high-priority operational improvements."
            )
        })

    except Exception as e:

        print(
            f"Real recommendation analysis unavailable: {e}"
        )

    return insights
if __name__ == "__main__":

    results = generate_insights()

    print("=" * 60)
    print("OPSLENS AI - AI INSIGHT ENGINE")
    print("=" * 60)

    for i, item in enumerate(results, start=1):

        print(f"\n{i}. [{item['severity']}] {item['category']}")

        print(
            f"Insight: {item['insight']}"
        )

        print(
            f"Recommendation: {item['recommendation']}"
        )

    print("\n" + "=" * 60)
    print("Insight generation completed successfully!")
    print("=" * 60)