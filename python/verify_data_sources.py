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

        print("=" * 65)
        print("OPSLENS AI - DATA SOURCE VERIFICATION")
        print("=" * 65)

        # Synthetic data
        cursor.execute("""
            SELECT COUNT(*)
            FROM orders;
        """)

        synthetic_count = cursor.fetchone()[0]

        # Real data
        cursor.execute("""
            SELECT COUNT(*)
            FROM real_delivery_orders;
        """)

        real_count = cursor.fetchone()[0]

        print(
            f"\nSynthetic orders:      {synthetic_count:,}"
        )

        print(
            f"Real delivery orders:  {real_count:,}"
        )

        print("\nData source separation:")

        if synthetic_count > 0 and real_count == 45584:
            print("PASS - Both datasets are present separately.")
        else:
            print("CHECK REQUIRED - Unexpected row counts.")

        print("\nSynthetic table: orders")
        print("Real table:      real_delivery_orders")

        print("\nNo tables were modified.")

finally:
    connection.close()