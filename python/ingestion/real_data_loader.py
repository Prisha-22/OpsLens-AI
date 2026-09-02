import os
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate geographical distance using
    the Haversine formula.
    """

    earth_radius = 6371

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1 - a)
    )

    return earth_radius * c


def load_real_data():

    # ==========================================
    # FILE PATH
    # ==========================================

    file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../data/real_data/Zomato Dataset.csv"
        )
    )

    # ==========================================
    # LOAD RAW DATA
    # ==========================================

    df = pd.read_csv(file_path)

    # ==========================================
    # STANDARDIZE COLUMN NAMES
    # ==========================================

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    # ==========================================
    # RENAME IMPORTANT COLUMNS
    # ==========================================

    df = df.rename(
        columns={
            "id": "order_id",
            "delivery_person_id": "rider_id",
            "delivery_person_age": "rider_age",
            "delivery_person_ratings": "rider_rating",
            "weather_conditions": "weather",
            "road_traffic_density": "traffic_level",
            "type_of_order": "order_type",
            "type_of_vehicle": "vehicle_type",
            "time_taken_min": "actual_delivery_minutes"
        }
    )

    # ==========================================
    # CLEAN TEXT COLUMNS
    # ==========================================

    text_columns = [
        "weather",
        "traffic_level",
        "festival",
        "city",
        "order_type",
        "vehicle_type",
        "rider_id"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        df[column] = df[column].replace(
            {
                "nan": pd.NA,
                "NaN": pd.NA,
                "None": pd.NA
            }
        )

    # ==========================================
    # HANDLE MISSING VALUES
    # ==========================================

    df["weather"] = df[
        "weather"
    ].fillna("Unknown")

    df["traffic_level"] = df[
        "traffic_level"
    ].fillna("Unknown")

    df["festival"] = df[
        "festival"
    ].fillna("Unknown")

    df["city"] = df[
        "city"
    ].fillna("Unknown")

    df["multiple_deliveries"] = df[
        "multiple_deliveries"
    ].fillna(
        df["multiple_deliveries"].median()
    )

    df["rider_age"] = df[
        "rider_age"
    ].fillna(
        df["rider_age"].median()
    )

    df["rider_rating"] = df[
        "rider_rating"
    ].fillna(
        df["rider_rating"].median()
    )

    # ==========================================
    # CONVERT NUMERIC COLUMNS
    # ==========================================

    numeric_columns = [
        "restaurant_latitude",
        "restaurant_longitude",
        "delivery_location_latitude",
        "delivery_location_longitude",
        "rider_age",
        "rider_rating",
        "vehicle_condition",
        "multiple_deliveries",
        "actual_delivery_minutes"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # ==========================================
    # CALCULATE DISTANCE
    # ==========================================

    df["distance_km"] = calculate_distance(
        df["restaurant_latitude"],
        df["restaurant_longitude"],
        df["delivery_location_latitude"],
        df["delivery_location_longitude"]
    )

    df["distance_km"] = df[
        "distance_km"
    ].round(2)

    # ==========================================
    # DISTANCE VALIDATION
    # ==========================================

    # Food-delivery distances above 50 km are
    # considered unrealistic for this dataset.
    invalid_distance = (
        df["distance_km"].isna()
        | (df["distance_km"] <= 0)
        | (df["distance_km"] > 50)
    )

    invalid_count = invalid_distance.sum()

    df.loc[
        invalid_distance,
        "distance_km"
    ] = pd.NA

    # Keep all orders by imputing invalid distance
    # with the median of valid delivery distances.
    valid_distance_median = df[
        "distance_km"
    ].median()

    df["distance_km"] = df[
        "distance_km"
    ].fillna(valid_distance_median)

    df["distance_km"] = df[
        "distance_km"
    ].round(2)

    # ==========================================
    # DATE / TIME PROCESSING
    # ==========================================

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    # ==========================================
    # CREATE PEAK HOUR FEATURE
    # ==========================================

    df["time_order_picked"] = (
        df["time_order_picked"]
        .astype("string")
        .str.strip()
    )

    picked_time = pd.to_datetime(
        df["time_order_picked"],
        format="%H:%M:%S",
        errors="coerce"
    )

    # Some datasets may contain HH:MM instead
    missing_time = picked_time.isna()

    picked_time.loc[missing_time] = pd.to_datetime(
        df.loc[
            missing_time,
            "time_order_picked"
        ],
        format="%H:%M",
        errors="coerce"
    )

    df["pickup_hour"] = picked_time.dt.hour

    df["peak_hour"] = np.where(
        df["pickup_hour"].isin(
            [12, 13, 14, 18, 19, 20, 21, 22]
        ),
        "Yes",
        "No"
    )

    # ==========================================
    # WEEKEND FEATURE
    # ==========================================

    df["weekend"] = np.where(
        df["order_date"].dt.dayofweek >= 5,
        "Yes",
        "No"
    )

    # ==========================================
    # FINAL VALIDATION
    # ==========================================

    required_columns = [
        "order_id",
        "rider_id",
        "distance_km",
        "weather",
        "traffic_level",
        "order_type",
        "vehicle_type",
        "actual_delivery_minutes",
        "city"
    ]

    df = df.dropna(
        subset=required_columns
    )

    print(
        f"\nInvalid GPS distances corrected: "
        f"{invalid_count:,}"
    )
        
    return df


if __name__ == "__main__":

    df = load_real_data()

    print("=" * 60)
    print("OPSLENS AI - REAL DATA LOADER")
    print("=" * 60)

    print(
        f"\nFinal Dataset Shape: "
        f"{df.shape}"
    )

    print("\nColumns:")

    print(
        df.columns.tolist()
    )

    print("\nMissing Values:")

    print(
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
        .head(15)
    )

    print("\nSample Data:")

    print(
        df[
            [
                "order_id",
                "rider_id",
                "distance_km",
                "weather",
                "traffic_level",
                "multiple_deliveries",
                "peak_hour",
                "weekend",
                "actual_delivery_minutes"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print(
        "\nReal data cleaning completed successfully!"
    )