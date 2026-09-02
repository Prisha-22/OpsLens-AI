import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from database import get_connection


def run_kpi_dashboard():

    conn = get_connection()

    customers = pd.read_sql("SELECT * FROM customers;", conn)
    restaurants = pd.read_sql("SELECT * FROM restaurants;", conn)
    riders = pd.read_sql("SELECT * FROM riders;", conn)
    orders = pd.read_sql("SELECT * FROM orders;", conn)
    payments = pd.read_sql("SELECT * FROM payments;", conn)

    conn.close()

    print("\n" + "=" * 60)
    print("           OPSLENS AI KPI DASHBOARD")
    print("=" * 60)

    print(f"👥 Total Customers        : {len(customers)}")
    print(f"🍽 Total Restaurants      : {len(restaurants)}")
    print(f"🚴 Total Riders           : {len(riders)}")
    print(f"📦 Total Orders           : {len(orders)}")

    print()

    print(f"💰 Total Revenue          : ₹{orders['order_value'].sum():,.2f}")
    print(f"💳 Total Payments         : ₹{payments['amount'].sum():,.2f}")

    print()

    print(f"⭐ Avg Restaurant Rating  : {restaurants['rating'].mean():.2f}")
    print(f"⭐ Avg Rider Rating       : {riders['rating'].mean():.2f}")

    print()

    print(f"🚚 Avg Delivery Time      : {orders['actual_delivery_minutes'].mean():.2f} mins")

    cancelled = (orders["delivery_status"] == "Cancelled").sum()
    cancellation_rate = cancelled / len(orders) * 100

    print(f"❌ Cancellation Rate      : {cancellation_rate:.2f}%")

    print("=" * 60)