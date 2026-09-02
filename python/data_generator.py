from database import get_connection
from generate_customers import generate_customers
from generate_restaurants import generate_restaurants
from generate_riders import generate_riders
from generate_orders import generate_orders
from generate_payments import generate_payments
from generate_ratings import generate_ratings

conn = get_connection()
cur = conn.cursor()

# Delete child tables first
cur.execute("DELETE FROM ratings;")
cur.execute("DELETE FROM payments;")
cur.execute("DELETE FROM orders;")

conn.commit()
cur.close()
conn.close()

print("=" * 50)
print("      OpsLens AI Data Generator")
print("=" * 50)

print("\nGenerating Customers...")
generate_customers()

print("\nGenerating Restaurants...")
generate_restaurants()

print("\nGenerating Riders...")
generate_riders()

print("\nGenerating Orders...")
generate_orders()

print("\nGenerating Payments...")
generate_payments()

print("\nGenerating Ratings...")
generate_ratings()

print("\n🎉 Database populated successfully!")