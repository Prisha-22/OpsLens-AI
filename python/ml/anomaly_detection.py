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
from sklearn.ensemble import IsolationForest

from database import get_connection


def detect_anomalies():

    # ==============================
    # Load Orders
    # ==============================

    conn = get_connection()

    query = """
    SELECT
        order_id,
        distance_km,
        order_value,
        delivery_fee,
        discount,
        actual_delivery_minutes,
        weather,
        traffic_level,
        delivery_status
    FROM orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==============================
    # Features
    # ==============================

    features = [
        "distance_km",
        "order_value",
        "delivery_fee",
        "discount",
        "actual_delivery_minutes"
    ]

    X = df[features].copy()

    # ==============================
    # Isolation Forest
    # ==============================

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(X)

    # ==============================
    # Anomaly Score
    # ==============================

    scores = model.decision_function(X)

    df["anomaly"] = predictions

    df["anomaly_score"] = scores

    df["anomaly_status"] = df["anomaly"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # ==============================
    # Extract Anomalies
    # ==============================

    anomalies = df[
        df["anomaly_status"] == "Anomaly"
    ].copy()

    # Lower score = more unusual
    anomalies = anomalies.sort_values(
        by="anomaly_score",
        ascending=True
    )

    return anomalies


if __name__ == "__main__":

    anomalies = detect_anomalies()

    print("=" * 50)
    print("OPSLENS AI - ANOMALY DETECTION")
    print("=" * 50)

    print(
        f"\nTotal anomalies detected: "
        f"{len(anomalies)}"
    )

    print("\nMost unusual anomalies:")

    print(
        anomalies[
            [
                "order_id",
                "anomaly_score",
                "distance_km",
                "order_value",
                "actual_delivery_minutes",
                "weather",
                "traffic_level",
                "delivery_status"
            ]
        ].head(10).to_string(index=False)
    )