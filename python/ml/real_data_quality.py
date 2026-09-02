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
from sklearn.ensemble import IsolationForest

from python.database import get_connection


def detect_real_anomalies():

    # ==========================================
    # LOAD REAL DELIVERY DATA
    # ==========================================

    conn = get_connection()

    query = """
    SELECT
        order_id,
        rider_id,
        distance_km,
        actual_delivery_minutes,
        rider_age,
        rider_rating,
        vehicle_condition,
        multiple_deliveries,
        pickup_hour,
        weather,
        traffic_level,
        city
    FROM real_delivery_orders;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # ==========================================
    # DATA QUALITY FLAGS
    # ==========================================

    df["data_quality_issue"] = False

    df.loc[
        (df["rider_age"] < 18) |
        (df["rider_age"] > 60),
        "data_quality_issue"
    ] = True

    df.loc[
        (df["rider_rating"] < 1) |
        (df["rider_rating"] > 5),
        "data_quality_issue"
    ] = True

    # ==========================================
    # OPERATIONAL FEATURES
    # ==========================================

    features = [
        "distance_km",
        "actual_delivery_minutes",
        "vehicle_condition",
        "multiple_deliveries",
        "pickup_hour"
    ]

    X = df[features].copy()

    X = X.fillna(
        X.median()
    )

    # ==========================================
    # ISOLATION FOREST
    # ==========================================

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(X)

    # ==========================================
    # ANOMALY SCORE
    # ==========================================

    scores = model.decision_function(X)

    df["anomaly"] = predictions

    df["anomaly_score"] = scores

    df["anomaly_status"] = df[
        "anomaly"
    ].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # ==========================================
    # EXTRACT OPERATIONAL ANOMALIES
    # ==========================================

    anomalies = df[
        df["anomaly_status"] == "Anomaly"
    ].copy()

    anomalies = anomalies.sort_values(
        by="anomaly_score",
        ascending=True
    )

    return anomalies


if __name__ == "__main__":

    anomalies = detect_real_anomalies()

    print("=" * 60)
    print("OPSLENS AI - REAL DATA OPERATIONAL ANOMALY DETECTION")
    print("=" * 60)

    print(
        f"\nTotal operational anomalies: "
        f"{len(anomalies):,}"
    )

    print(
        f"Anomaly rate: "
        f"{len(anomalies) / 45584 * 100:.2f}%"
    )

    print(
        f"\nAnomalies containing data-quality issues: "
        f"{anomalies['data_quality_issue'].sum():,}"
    )

    print("\nMost unusual operational anomalies:")

    print(
        anomalies[
            [
                "order_id",
                "anomaly_score",
                "distance_km",
                "actual_delivery_minutes",
                "multiple_deliveries",
                "vehicle_condition",
                "pickup_hour",
                "weather",
                "traffic_level",
                "city",
                "data_quality_issue"
            ]
        ]
        .head(15)
        .to_string(index=False)
    )

    print(
        "\nReal operational anomaly detection "
        "completed successfully!"
    )