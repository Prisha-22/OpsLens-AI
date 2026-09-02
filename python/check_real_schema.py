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
            SELECT
                column_name,
                data_type
            FROM information_schema.columns
            WHERE table_name = 'zomato_real_orders'
            ORDER BY ordinal_position;
        """)

        rows = cursor.fetchall()

        print("=" * 60)
        print("OPSLENS AI - REAL ZOMATO TABLE SCHEMA")
        print("=" * 60)

        for column_name, data_type in rows:
            print(
                f"{column_name:<35} {data_type}"
            )

finally:
    connection.close()