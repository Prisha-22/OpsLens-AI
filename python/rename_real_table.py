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
            ALTER TABLE zomato_real_orders
            RENAME TO real_delivery_orders;
        """)

    connection.commit()

    print("=" * 60)
    print("OPSLENS AI - REAL DATA TABLE RENAME")
    print("=" * 60)
    print("\nTable renamed successfully:")
    print("zomato_real_orders → real_delivery_orders")

finally:
    connection.close()