import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

import joblib
import pandas as pd


# ==========================================
# LOAD SAVED MODEL
# ==========================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "delivery_time_model.pkl"
)

model = joblib.load(model_path)


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_delivery_time(
    distance,
    weather,
    traffic,
    peak_hour,
    weekend,
    order_value,
    delivery_fee,
    discount
):

    sample = pd.DataFrame({
        "distance_km": [distance],
        "weather": [weather],
        "traffic_level": [traffic],
        "peak_hour": [peak_hour == "Yes"],
        "weekend": [weekend == "Yes"],
        "order_type": ["Delivery"],
        "delivery_fee": [delivery_fee],
        "discount": [discount]
    })

    prediction = model.predict(sample)

    return float(prediction[0])


# ==========================================
# TEST PREDICTION
# ==========================================

if __name__ == "__main__":

    prediction = predict_delivery_time(
        distance=8,
        weather="Rainy",
        traffic="High",
        peak_hour="Yes",
        weekend="No",
        order_value=500,
        delivery_fee=45,
        discount=20
    )

    print("=" * 50)
    print("DELIVERY TIME PREDICTION")
    print("=" * 50)

    print(
        f"Predicted Delivery Time: "
        f"{prediction:.2f} minutes"
    )