from faker import Faker
import random
from database import get_connection

fake = Faker("en_IN")


def generate_riders():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM riders;")

    cities = [
        "Chennai",
        "Bangalore",
        "Mumbai",
        "Hyderabad",
        "Delhi"
    ]

    vehicles = [
        "Bike",
        "Scooter",
        "Bicycle"
    ]

    for i in range(1, 101):

        rider_id = f"D{i:03d}"
        rider_name = fake.name()
        city = random.choice(cities)
        vehicle_type = random.choice(vehicles)
        joining_date = fake.date_between(start_date="-4y", end_date="today")
        rating = round(random.uniform(3.8, 5.0), 1)

        cur.execute("""
            INSERT INTO riders
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            rider_id,
            rider_name,
            city,
            vehicle_type,
            joining_date,
            rating
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Riders generated successfully!")