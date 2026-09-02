from database import get_connection
import random

feedbacks = [
    "Excellent service",
    "Fast delivery",
    "Food was hot",
    "Packaging was good",
    "Late delivery",
    "Average experience",
    "Very polite rider",
    "Restaurant delayed preparation",
    "Will order again",
    "Not satisfied"
]

def generate_ratings():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM ratings;")

    for i in range(1,10001):

        rating_id = f"RT{i:05d}"

        order_id = f"O{i:05d}"

        customer_rating = random.randint(1,5)

        rider_rating = random.randint(1,5)

        restaurant_rating = random.randint(1,5)

        feedback = random.choice(feedbacks)

        cur.execute("""
        INSERT INTO ratings
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            rating_id,
            order_id,
            customer_rating,
            rider_rating,
            restaurant_rating,
            feedback
        ))

    conn.commit()

    cur.close()
    conn.close()

    print("✅ Ratings generated successfully!")