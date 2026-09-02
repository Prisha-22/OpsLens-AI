from faker import Faker
import random
from database import get_connection

fake = Faker("en_IN")


def generate_restaurants():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM restaurants;")

    cuisines = [
        "North Indian",
        "South Indian",
        "Chinese",
        "Italian",
        "Fast Food",
        "Cafe",
        "Biryani",
        "Desserts"
    ]

    cities = [
        "Chennai",
        "Bangalore",
        "Mumbai",
        "Hyderabad",
        "Delhi"
    ]

    for i in range(1, 51):

        restaurant_id = f"R{i:03d}"
        restaurant_name = fake.company() + " Restaurant"
        city = random.choice(cities)
        cuisine = random.choice(cuisines)
        rating = round(random.uniform(3.5, 5.0), 1)
        opening_year = random.randint(2015, 2025)
        avg_preparation_time = random.randint(15, 60)

        cur.execute("""
            INSERT INTO restaurants
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            restaurant_id,
            restaurant_name,
            city,
            cuisine,
            rating,
            opening_year,
            avg_preparation_time
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Restaurants generated successfully!")