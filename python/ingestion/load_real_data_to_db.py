import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

import pandas as pd

from real_data_loader import load_real_data
from database import get_connection


def create_real_data_table(cursor):

    query = """
    DROP TABLE IF EXISTS real_delivery_orders;

    CREATE TABLE real_delivery_orders (

        order_id VARCHAR(50) PRIMARY KEY,

        rider_id VARCHAR(100),

        rider_age FLOAT,
        rider_rating FLOAT,

        restaurant_latitude FLOAT,
        restaurant_longitude FLOAT,

        delivery_location_latitude FLOAT,
        delivery_location_longitude FLOAT,

        order_date DATE,

        time_orderd VARCHAR(20),
        time_order_picked VARCHAR(20),

        pickup_hour FLOAT,

        distance_km FLOAT,

        weather VARCHAR(50),
        traffic_level VARCHAR(50),

        vehicle_condition INT,
        order_type VARCHAR(50),
        vehicle_type VARCHAR(50),

        multiple_deliveries FLOAT,

        festival VARCHAR(20),
        city VARCHAR(50),

        peak_hour VARCHAR(10),
        weekend VARCHAR(10),

        actual_delivery_minutes FLOAT
    );
    """

    cursor.execute(query)


def load_real_data_to_database():

    print("=" * 65)
    print("OPSLENS AI - REAL DATA DATABASE LOADER")
    print("=" * 65)

    # ==========================================
    # LOAD CLEAN REAL DATA
    # ==========================================

    print("\nLoading cleaned Zomato dataset...")

    df = load_real_data()

    print(
        f"Real orders loaded: "
        f"{len(df):,}"
    )

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    conn = get_connection()

    cursor = conn.cursor()

    # ==========================================
    # CREATE TABLE
    # ==========================================

    print(
        "\nCreating real_delivery_orders table..."
    )

    create_real_data_table(cursor)

    conn.commit()

    # ==========================================
    # PREPARE INSERT
    # ==========================================

    insert_query = """
    INSERT INTO real_delivery_orders (

        order_id,
        rider_id,

        rider_age,
        rider_rating,

        restaurant_latitude,
        restaurant_longitude,

        delivery_location_latitude,
        delivery_location_longitude,

        order_date,

        time_orderd,
        time_order_picked,

        pickup_hour,

        distance_km,

        weather,
        traffic_level,

        vehicle_condition,
        order_type,
        vehicle_type,

        multiple_deliveries,

        festival,
        city,

        peak_hour,
        weekend,

        actual_delivery_minutes

    )
    VALUES (
        %s, %s,
        %s, %s,
        %s, %s,
        %s, %s,
        %s,
        %s, %s,
        %s,
        %s,
        %s, %s,
        %s, %s, %s,
        %s,
        %s, %s,
        %s, %s,
        %s
    );
    """

    # ==========================================
    # INSERT DATA
    # ==========================================

    print(
        "\nInserting real operational records..."
    )

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                str(row["order_id"]),
                str(row["rider_id"]),

                float(row["rider_age"]),
                float(row["rider_rating"]),

                float(row["restaurant_latitude"]),
                float(row["restaurant_longitude"]),

                float(
                    row[
                        "delivery_location_latitude"
                    ]
                ),

                float(
                    row[
                        "delivery_location_longitude"
                    ]
                ),

                row["order_date"],

                (
                    str(row["time_orderd"])
                    if pd.notna(
                        row["time_orderd"]
                    )
                    else None
                ),

                str(
                    row["time_order_picked"]
                ),

                (
                    float(row["pickup_hour"])
                    if pd.notna(
                        row["pickup_hour"]
                    )
                    else None
                ),

                float(row["distance_km"]),

                str(row["weather"]),
                str(row["traffic_level"]),

                int(row["vehicle_condition"]),

                str(row["order_type"]),
                str(row["vehicle_type"]),

                float(
                    row[
                        "multiple_deliveries"
                    ]
                ),

                str(row["festival"]),
                str(row["city"]),

                str(row["peak_hour"]),
                str(row["weekend"]),

                float(
                    row[
                        "actual_delivery_minutes"
                    ]
                )
            )
        )

    cursor.executemany(
        insert_query,
        records
    )

    conn.commit()

    # ==========================================
    # VERIFY
    # ==========================================

    cursor.execute(
        "SELECT COUNT(*) FROM real_delivery_orders;"
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print(
        f"\nRecords successfully inserted: "
        f"{count:,}"
    )

    print("\n" + "=" * 65)
    print(
        "REAL DATA LOADED INTO OPSLENS AI SUCCESSFULLY!"
    )
    print("=" * 65)


if __name__ == "__main__":

    load_real_data_to_database()