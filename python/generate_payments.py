from database import get_connection
from faker import Faker
import random
from datetime import timedelta

fake = Faker("en_IN")

def generate_payments():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM payments;")

    payment_modes = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Cash",
        "Wallet"
    ]

    payment_statuses = [
        "Success",
        "Success",
        "Success",
        "Success",
        "Refunded",
        "Failed"
    ]

    for i in range(1,10001):

        payment_id = f"P{i:05d}"

        order_id = f"O{i:05d}"

        payment_mode = random.choice(payment_modes)

        payment_status = random.choice(payment_statuses)

        amount = round(random.uniform(150,1800),2)

        transaction_time = fake.date_time_between(
            start_date="-365d",
            end_date="now"
        )

        cur.execute("""
        INSERT INTO payments
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            payment_id,
            order_id,
            payment_mode,
            amount,
            payment_status,
            transaction_time
        ))

    conn.commit()

    cur.close()
    conn.close()

    print("✅ Payments generated successfully!")