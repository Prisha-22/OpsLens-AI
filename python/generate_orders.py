from database import get_connection
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("en_IN")


def generate_orders():

    conn = get_connection()
    cur = conn.cursor()

    # Clear old data
    cur.execute("DELETE FROM orders;")

    # Generate 10,000 orders
    for i in range(1, 10001):

        # Primary Key
        order_id = f"O{i:05d}"

        # Foreign Keys
        customer_id = f"C{random.randint(1,500):04d}"
        restaurant_id = f"R{random.randint(1,50):03d}"
        rider_id = f"D{random.randint(1,100):03d}"

        # TEMP values (we'll replace these later)
        # Random order date within the last year
        order_time = fake.date_time_between(
            start_date="-365d",
            end_date="now"
        )

        # Restaurant preparation time
        prep_time = random.randint(8, 25)

        pickup_time = order_time + timedelta(minutes=prep_time)

        estimated_delivery_minutes = random.randint(20, 45)

        actual_delivery_minutes = estimated_delivery_minutes + random.randint(-5, 20)

        if actual_delivery_minutes < 10:
            actual_delivery_minutes = 10

        delivery_time = pickup_time + timedelta(minutes=actual_delivery_minutes)
        distance_km = round(random.uniform(1.0, 15.0), 2)

        weather = random.choices(
            ["Sunny", "Cloudy", "Rainy", "Foggy"],
            weights=[45, 25, 20, 10]
        )[0]

        traffic_level = random.choices(
            ["Low", "Medium", "High"],
            weights=[25, 45, 30]
        )[0]

        hour = order_time.hour

        peak_hour = (
            (12 <= hour <= 14) or
            (19 <= hour <= 22)
        )
        weekend = order_time.weekday() >= 5

        order_type = "Food"

        order_value = round(random.uniform(150, 1800), 2)

        delivery_fee = round(random.uniform(20, 80), 2)

        discount = round(random.uniform(0, 250), 2)

        delivery_status = random.choices(
            ["Delivered", "Delayed", "Cancelled"],
            weights=[88, 8, 4]
        )[0]

        if delivery_status == "Cancelled":
            cancellation_reason = random.choice([
                "Customer Cancelled",
                "Restaurant Closed",
                "No Rider Available",
                "Payment Failed"
            ])
        else:
            cancellation_reason = None

        cur.execute("""
            INSERT INTO orders
            VALUES (
                %s,%s,%s,%s,
                %s,%s,%s,
                %s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s
            )
        """, (
            order_id,
            customer_id,
            restaurant_id,
            rider_id,
            order_time,
            pickup_time,
            delivery_time,
            estimated_delivery_minutes,
            actual_delivery_minutes,
            distance_km,
            weather,
            traffic_level,
            peak_hour,
            weekend,
            order_type,
            order_value,
            delivery_fee,
            discount,
            delivery_status,
            cancellation_reason
        ))

    conn.commit()

    cur.close()
    conn.close()

    print("✅ 10,000 Orders generated successfully!")