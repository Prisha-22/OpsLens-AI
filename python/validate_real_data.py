import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(PROJECT_ROOT)

from python.database import get_connection


connection = get_connection()

try:
    with connection.cursor() as cursor:

        print("=" * 60)
        print("OPSLENS AI - REAL ZOMATO DATA VALIDATION")
        print("=" * 60)

        # Row count
        cursor.execute("""
            SELECT COUNT(*)
            FROM zomato_real_orders;
        """)

        row_count = cursor.fetchone()[0]

        print(f"\nTotal rows: {row_count:,}")

        # Key null checks
        cursor.execute("""
            SELECT
                COUNT(*) FILTER (WHERE order_id IS NULL),
                COUNT(*) FILTER (WHERE rider_id IS NULL),
                COUNT(*) FILTER (WHERE distance_km IS NULL),
                COUNT(*) FILTER (WHERE actual_delivery_minutes IS NULL),
                COUNT(*) FILTER (WHERE weather IS NULL),
                COUNT(*) FILTER (WHERE traffic_level IS NULL),
                COUNT(*) FILTER (WHERE city IS NULL)
            FROM zomato_real_orders;
        """)

        nulls = cursor.fetchone()

        print("\nKey NULL counts:")

        labels = [
            "order_id",
            "rider_id",
            "distance_km",
            "actual_delivery_minutes",
            "weather",
            "traffic_level",
            "city"
        ]

        for label, value in zip(labels, nulls):
            print(f"{label:<30} {value}")

        # Distance statistics
        cursor.execute("""
            SELECT
                MIN(distance_km),
                MAX(distance_km),
                ROUND(AVG(distance_km), 2)
            FROM zomato_real_orders;
        """)

        min_distance, max_distance, avg_distance = cursor.fetchone()

        print("\nDistance statistics:")
        print(f"Minimum distance: {min_distance} km")
        print(f"Maximum distance: {max_distance} km")
        print(f"Average distance: {avg_distance} km")

        # Delivery time statistics
        cursor.execute("""
            SELECT
                MIN(actual_delivery_minutes),
                MAX(actual_delivery_minutes),
                ROUND(AVG(actual_delivery_minutes), 2)
            FROM zomato_real_orders;
        """)

        min_delivery, max_delivery, avg_delivery = cursor.fetchone()

        print("\nDelivery time statistics:")
        print(f"Minimum: {min_delivery} minutes")
        print(f"Maximum: {max_delivery} minutes")
        print(f"Average: {avg_delivery} minutes")

        # Duplicate order IDs
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT order_id
                FROM zomato_real_orders
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) duplicates;
        """)

        duplicate_ids = cursor.fetchone()[0]

        print(
            f"\nDuplicate order IDs: {duplicate_ids}"
        )

        print("\nValidation completed successfully.")

finally:
    connection.close()