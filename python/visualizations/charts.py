import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib.pyplot as plt
import pandas as pd

from database import get_connection


def generate_charts():

    conn = get_connection()

    customers = pd.read_sql("SELECT * FROM customers;", conn)
    orders = pd.read_sql("SELECT * FROM orders;", conn)
    restaurants = pd.read_sql("SELECT * FROM restaurants;", conn)
    riders = pd.read_sql("SELECT * FROM riders;", conn)
    payments = pd.read_sql("SELECT * FROM payments;", conn)

    conn.close()

    charts_folder = os.path.join(
        os.path.dirname(__file__),
        "..",
        "reports",
        "charts"
    )

    os.makedirs(charts_folder, exist_ok=True)

    print("\nGenerating Charts...")

    # =====================================================
    # Customer Membership Distribution
    # =====================================================

    plt.figure(figsize=(8,5))
    customers["membership"].value_counts().plot(kind="bar")
    plt.title("Customer Membership Distribution")
    plt.xlabel("Membership")
    plt.ylabel("Number of Customers")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"customer_membership_distribution.png"))
    plt.close()

    # =====================================================
    # Customers by City
    # =====================================================

    plt.figure(figsize=(8,5))
    customers["city"].value_counts().plot(kind="bar")
    plt.title("Customers by City")
    plt.xlabel("City")
    plt.ylabel("Customers")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"customers_by_city.png"))
    plt.close()

    # =====================================================
    # Orders by Weather
    # =====================================================

    plt.figure(figsize=(8,5))
    orders["weather"].value_counts().plot(kind="bar")
    plt.title("Orders by Weather")
    plt.xlabel("Weather")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"weather_distribution.png"))
    plt.close()

    # =====================================================
    # Traffic Distribution
    # =====================================================

    plt.figure(figsize=(8,5))
    orders["traffic_level"].value_counts().plot(kind="bar")
    plt.title("Traffic Distribution")
    plt.xlabel("Traffic Level")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"traffic_distribution.png"))
    plt.close()

    # =====================================================
    # Restaurant Cuisine
    # =====================================================

    plt.figure(figsize=(8,5))
    restaurants["cuisine"].value_counts().plot(kind="bar")
    plt.title("Cuisine Distribution")
    plt.xlabel("Cuisine")
    plt.ylabel("Restaurants")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"cuisine_distribution.png"))
    plt.close()

    # =====================================================
    # Rider Vehicle Types
    # =====================================================

    plt.figure(figsize=(6,6))
    riders["vehicle_type"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%"
    )
    plt.ylabel("")
    plt.title("Vehicle Type Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"vehicle_types.png"))
    plt.close()

    # =====================================================
    # Payment Modes
    # =====================================================

    plt.figure(figsize=(8,5))
    payments["payment_mode"].value_counts().plot(kind="bar")
    plt.title("Payment Mode Distribution")
    plt.xlabel("Payment Mode")
    plt.ylabel("Transactions")
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder,"payment_modes.png"))
    plt.close()

    print("✅ All charts generated successfully!")