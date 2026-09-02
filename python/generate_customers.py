from faker import Faker
import random
from database import get_connection

fake = Faker("en_IN")


def generate_customers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM customers;")

    cities = [
        "Chennai",
        "Bangalore",
        "Hyderabad",
        "Mumbai",
        "Delhi"
    ]

    zones = [
        "North",
        "South",
        "East",
        "West",
        "Central"
    ]

    memberships = [
        "Regular",
        "Gold",
        "Silver",
        "Premium"
    ]

    for i in range(1, 501):

        customer_id = f"C{i:04d}"
        customer_name = fake.name()
        city = random.choice(cities)
        zone = random.choice(zones)
        signup_date = fake.date_between(start_date="-3y", end_date="today")
        membership = random.choice(memberships)
        total_orders = random.randint(1, 150)

        cur.execute("""
            INSERT INTO customers
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            customer_id,
            customer_name,
            city,
            zone,
            signup_date,
            membership,
            total_orders
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Customers generated successfully!")