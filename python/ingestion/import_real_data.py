import sys
import os

import pandas as pd
from psycopg2.extras import execute_values

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(PROJECT_ROOT)

from python.database import get_connection
from python.ingestion.real_data_loader import load_real_data

TABLE_NAME = "zomato_real_orders"


def create_table(connection):
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (

        order_id VARCHAR,
        rider_id VARCHAR,

        rider_age NUMERIC,
        rider_rating NUMERIC,

        restaurant_latitude NUMERIC,
        restaurant_longitude NUMERIC,

        delivery_location_latitude NUMERIC,
        delivery_location_longitude NUMERIC,

        order_date DATE,

        time_orderd VARCHAR,
        time_order_picked VARCHAR,

        weather VARCHAR,
        traffic_level VARCHAR,

        vehicle_condition NUMERIC,
        order_type VARCHAR,
        vehicle_type VARCHAR,

        multiple_deliveries NUMERIC,
        festival VARCHAR,
        city VARCHAR,

        actual_delivery_minutes INTEGER,
        distance_km NUMERIC,

        pickup_hour INTEGER,
        peak_hour VARCHAR,
        weekend VARCHAR
    );
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

    connection.commit()


def insert_data(connection, df):

    columns = [
        "order_id",
        "rider_id",
        "rider_age",
        "rider_rating",
        "restaurant_latitude",
        "restaurant_longitude",
        "delivery_location_latitude",
        "delivery_location_longitude",
        "order_date",
        "time_orderd",
        "time_order_picked",
        "weather",
        "traffic_level",
        "vehicle_condition",
        "order_type",
        "vehicle_type",
        "multiple_deliveries",
        "festival",
        "city",
        "actual_delivery_minutes",
        "distance_km",
        "pickup_hour",
        "peak_hour",
        "weekend"
    ]

    rows = []

    for row in df[columns].itertuples(index=False, name=None):

        cleaned_row = []

        for value in row:

            if pd.isna(value):
                cleaned_row.append(None)
            else:
                cleaned_row.append(value)

        rows.append(tuple(cleaned_row))

    query = f"""
        INSERT INTO {TABLE_NAME}
        ({", ".join(columns)})
        VALUES %s
    """

    with connection.cursor() as cursor:

        execute_values(
            cursor,
            query,
            rows,
            page_size=1000
        )

    connection.commit()


def main():

    print("=" * 60)
    print("OPSLENS AI - REAL ZOMATO DATA IMPORT")
    print("=" * 60)

    print("\nLoading cleaned real data...")

    df = load_real_data()

    print(
        f"Rows ready for import: {len(df):,}"
    )

    connection = get_connection()

    try:

        print(
            f"\nCreating PostgreSQL table: "
            f"{TABLE_NAME}"
        )

        create_table(connection)

        print(
            "\nImporting data..."
        )

        insert_data(
            connection,
            df
        )

        print(
            f"\nSuccessfully imported "
            f"{len(df):,} rows."
        )

    finally:

        connection.close()

    print(
        "\nReal Zomato data import completed!"
    )


if __name__ == "__main__":
    main()