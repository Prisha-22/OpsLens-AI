import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from data_preprocessing import load_data


# ============================
# Load Dataset
# ============================

df = load_data()

# Features
X = df.drop(columns=["actual_delivery_minutes"])

# Target
y = df["actual_delivery_minutes"]


# ============================
# Categorical Columns
# ============================

categorical_features = [
    "weather",
    "traffic_level",
    "peak_hour",
    "weekend",
    "order_type"
]

numeric_features = [
    "distance_km",
    "delivery_fee",
    "discount"
]


# ============================
# Preprocessing
# ============================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
        (
            "num",
            "passthrough",
            numeric_features,
        ),
    ]
)


# ============================
# Model
# ============================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# ============================
# Train Test Split
# ============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


# ============================
# Train
# ============================

print("\nTraining Model...")

pipeline.fit(X_train, y_train)

print("Model Trained Successfully!")


# ============================
# Evaluation
# ============================

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Performance")

print(f"MAE : {mae:.2f}")
print(f"R²  : {r2:.2f}")


# ============================
# Save Model
# ============================

model_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "delivery_time_model.pkl"
)

joblib.dump(pipeline, model_path)

print("\nModel Saved Successfully!")
print(model_path)