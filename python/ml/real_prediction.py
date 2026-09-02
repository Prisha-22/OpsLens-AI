import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

from python.database import get_connection


# ==========================================
# LOAD REAL DATA
# ==========================================

def load_real_data():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM real_delivery_orders;",
        conn
    )

    conn.close()

    return df


# ==========================================
# TRAIN REAL ML MODEL
# ==========================================

def train_real_prediction_model():

    df = load_real_data()

    features = [
        "distance_km",
        "rider_age",
        "rider_rating",
        "weather",
        "traffic_level",
        "vehicle_condition",
        "order_type",
        "vehicle_type",
        "multiple_deliveries",
        "festival",
        "city",
        "pickup_hour",
        "peak_hour",
        "weekend"
    ]

    target = "actual_delivery_minutes"

    df = df[features + [target]].copy()

    df = df.dropna()

    X = df[features]
    y = df[target]

    categorical_features = [
        "weather",
        "traffic_level",
        "order_type",
        "vehicle_type",
        "festival",
        "city",
        "peak_hour",
        "weekend"
    ]

    numeric_features = [
        "distance_km",
        "rider_age",
        "rider_rating",
        "vehicle_condition",
        "multiple_deliveries",
        "pickup_hour"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            )
        ]
    )

    model = RandomForestRegressor(
        n_estimators=150,
        random_state=42,
        n_jobs=-1,
        max_depth=15
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X, y)

    return pipeline


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_real_delivery_time(
    distance,
    rider_age,
    rider_rating,
    weather,
    traffic,
    vehicle_condition,
    order_type,
    vehicle_type,
    multiple_deliveries,
    festival,
    city,
    pickup_hour,
    peak_hour,
    weekend
):

    model = train_real_prediction_model()

    sample = pd.DataFrame({
        "distance_km": [distance],
        "rider_age": [rider_age],
        "rider_rating": [rider_rating],
        "weather": [weather],
        "traffic_level": [traffic],
        "vehicle_condition": [vehicle_condition],
        "order_type": [order_type],
        "vehicle_type": [vehicle_type],
        "multiple_deliveries": [multiple_deliveries],
        "festival": [festival],
        "city": [city],
        "pickup_hour": [pickup_hour],
        "peak_hour": [peak_hour],
        "weekend": [weekend]
    })

    prediction = model.predict(sample)

    return float(prediction[0])


# ==========================================
# TEST MODEL
# ==========================================

if __name__ == "__main__":

    prediction = predict_real_delivery_time(
        distance=8.0,
        rider_age=28,
        rider_rating=4.5,
        weather="Fog",
        traffic="Jam",
        vehicle_condition=1,
        order_type="Snack",
        vehicle_type="motorcycle",
        multiple_deliveries=1,
        festival="No",
        city="Metropolitian",
        pickup_hour=20,
        peak_hour="Yes",
        weekend="No"
    )

    print("=" * 60)
    print("OPSLENS AI - REAL DELIVERY TIME PREDICTION")
    print("=" * 60)

    print(
        f"Predicted Delivery Time: "
        f"{prediction:.2f} minutes"
    )