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
from analytics.root_cause_analysis import analyze_root_causes

def get_operational_health():
    # ------------------------------------------
    # Anomaly Detection
    # ------------------------------------------

    anomalies = detect_anomalies()
    anomaly_count = len(anomalies)
        # ------------------------------------------
    # Forecast
    # ------------------------------------------

    historical, forecast = generate_forecast()

    current_delivery_time = historical[
        "average_delivery_time"
    ].mean()

    forecast_delivery_time = forecast[
        "predicted_delivery_time"
    ].mean()

    forecast_change = (
        forecast_delivery_time - current_delivery_time
    )

    if forecast_change > 2:

        forecast_status = "Increasing"

    elif forecast_change < -2:

        forecast_status = "Improving"

    else:

        forecast_status = "Stable"

    # ------------------------------------------
    # Root Cause Analysis
    # ------------------------------------------

    root_causes = analyze_root_causes()

    # Find the strongest positive impact
    root_cause_candidates = []

    for factor_name in [
        "traffic",
        "weather",
        "peak",
        "weekend",
        "order_type",
        "distance"
    ]:

        factor_data = root_causes[factor_name]

        if not factor_data.empty:

            strongest = factor_data.iloc[0]

            root_cause_candidates.append({
                "category": factor_name,
                "factor": strongest["factor"],
                "impact": strongest["impact"]
            })

    # Find highest impact factor
    strongest_root_cause = max(
        root_cause_candidates,
        key=lambda x: x["impact"]
    )

    # ------------------------------------------
    # User-friendly root cause label
    # ------------------------------------------

    root_cause_labels = {
        "traffic": "Traffic",
        "weather": "Weather",
        "peak": "Peak Hour",
        "weekend": "Weekend",
        "order_type": "Order Type",
        "distance": "Distance"
    }

    root_cause_factor = root_cause_labels.get(
        strongest_root_cause["category"],
        str(strongest_root_cause["factor"])
    )

    conn = get_connection()

    query = """
    SELECT
        actual_delivery_minutes,
        delivery_status
    FROM orders;
    """

    orders = pd.read_sql(query, conn)

    conn.close()

    # ------------------------------------------
    # Average delivery time
    # ------------------------------------------

    average_delivery = orders[
        "actual_delivery_minutes"
    ].mean()

    # ------------------------------------------
    # Delayed orders
    # ------------------------------------------

    delayed_orders = len(
        orders[
            orders["delivery_status"] == "Delayed"
        ]
    )

    total_orders = len(orders)

    delayed_percentage = (
        delayed_orders / total_orders
    ) * 100

    # ------------------------------------------
    # Operational health status
    # ------------------------------------------

    if delayed_percentage >= 10:

        health_status = "Critical"

    elif delayed_percentage >= 5:

        health_status = "Needs Attention"

    else:

        health_status = "Healthy"

    return {
        "average_delivery": average_delivery,
        "delayed_orders": delayed_orders,
        "delayed_percentage": delayed_percentage,
        "total_orders": total_orders,
        "health_status": health_status,
        "anomaly_count": anomaly_count,
        "forecast_status": forecast_status,
        "forecast_delivery_time": forecast_delivery_time,
        "forecast_change": forecast_change,
        "root_cause_category": strongest_root_cause["category"],
        "root_cause_factor": root_cause_factor,
        "root_cause_impact": strongest_root_cause["impact"]
    }


if __name__ == "__main__":

    health = get_operational_health()

    print("=" * 50)
    print("OPSLENS AI - OPERATIONAL HEALTH")
    print("=" * 50)

    print(
        f"\nAverage Delivery Time: "
        f"{health['average_delivery']:.2f} minutes"
    )

    print(
        f"Delayed Orders: "
        f"{health['delayed_orders']:,}"
    )

    print(
        f"Delayed Percentage: "
        f"{health['delayed_percentage']:.2f}%"
    )

    print(
        f"Operational Status: "
        f"{health['health_status']}"
    )

    print(
        f"Anomalies Detected: "
        f"{health['anomaly_count']:,}"
    )

    print(
        f"Forecast Status: "
        f"{health['forecast_status']}"
    )

    print(
        f"Forecast Average: "
        f"{health['forecast_delivery_time']:.2f} minutes"
    )

    print(
        f"Forecast Change: "
        f"{health['forecast_change']:+.2f} minutes"
    )

    print(
        f"\nStrongest Root Cause: "
        f"{health['root_cause_factor']}"
    )

    print(
        f"Root Cause Category: "
        f"{health['root_cause_category']}"
    )

    print(
        f"Impact: "
        f"{health['root_cause_impact']:+.2f} minutes"
    )