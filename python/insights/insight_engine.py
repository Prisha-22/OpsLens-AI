from python.ml.real_anomaly_detection import detect_real_anomalies
from python.analytics.real_root_cause_analysis import analyze_real_root_causes
from python.insights.real_operational_health import calculate_operational_health
from python.insights.real_recommendation_engine import generate_real_recommendations


def generate_real_insights():
    """
    Generate AI-style operational insights from the real delivery dataset.
    """

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
                f"Real delivery operations have a health "
                f"score of {health_score}/100 with an "
                f"overall status of {status}."
            ),
            "recommendation": (
                "Prioritize the operational factors with "
                "the highest delivery-time impact."
            )
        })

    except Exception as e:
        print(f"Real operational health unavailable: {e}")

    # ==========================================
    # ROOT CAUSE ANALYSIS
    # ==========================================

    try:
        root_causes = analyze_real_root_causes()

        traffic = root_causes["traffic"]

        if not traffic.empty:
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

        if not multiple.empty:
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
        print(f"Real root cause analysis unavailable: {e}")

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
        print(f"Real anomaly analysis unavailable: {e}")

    # ==========================================
    # REAL RECOMMENDATIONS
    # ==========================================

    try:
        recommendations = generate_real_recommendations()

        critical_count = sum(
            1
            for recommendation in recommendations
            if recommendation.get("priority") == "Critical"
        )

        high_count = sum(
            1
            for recommendation in recommendations
            if recommendation.get("priority") == "High"
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
                "followed by high-priority operational "
                "improvements."
            )
        })

    except Exception as e:
        print(f"Real recommendation analysis unavailable: {e}")

    return insights


if __name__ == "__main__":
    print("=" * 60)
    print("        OpsLens AI - AI Insight Engine")
    print("=" * 60)

    print("\nGenerating real-data AI insights...")

    results = generate_real_insights()

    for i, item in enumerate(results, start=1):
        print(f"\n{i}. [{item['severity']}] {item['category']}")
        print(f"Insight: {item['insight']}")
        print(f"Recommendation: {item['recommendation']}")

    print("\n" + "=" * 60)
    print("Real-data insight generation completed!")
    print("=" * 60)