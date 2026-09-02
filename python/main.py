print("=" * 60)
print("        OpsLens AI - Real Data Analytics Engine")
print("=" * 60)

print("\nStarting real-data analytics...")

from analytics.real_root_cause_analysis import analyze_real_root_causes
from insights.real_operational_health import calculate_operational_health
from insights.real_recommendation_engine import generate_real_recommendations
from ml.real_anomaly_detection import detect_real_anomalies
from insights.insight_engine import generate_real_insights

print("\n1. Root Cause Analysis")
root_causes = analyze_real_root_causes()
print("Root cause analysis completed.")

print("\n2. Operational Health")
health = calculate_operational_health()
print(f"Health Score: {health['health_score']}/100")
print(f"Status: {health['status']}")

print("\n3. Anomaly Detection")
anomalies = detect_real_anomalies()
print(f"Anomalies detected: {len(anomalies)}")

print("\n4. AI Recommendations")
recommendations = generate_real_recommendations()
print(f"Recommendations generated: {len(recommendations)}")

print("\n5. AI Insights")
insights = generate_real_insights()
print(f"Insights generated: {len(insights)}")

print("\n" + "=" * 60)
print("Real-data analytics completed successfully!")
print("=" * 60)