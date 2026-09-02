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

        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'real_delivery_orders'
            );
        """)

        exists = cursor.fetchone()[0]

        print("=" * 60)
        print("OPSLENS AI - EXISTING REAL DATA TABLE CHECK")
        print("=" * 60)

        print(
            f"\nreal_delivery_orders exists: {exists}"
        )

finally:
    connection.close()