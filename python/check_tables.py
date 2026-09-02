import os
import sys

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database import get_connection


conn = get_connection()
cur = conn.cursor()

query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
"""

cur.execute(query)

tables = cur.fetchall()

print("=" * 50)
print("OPSLENS AI - DATABASE TABLES")
print("=" * 50)

for table in tables:
    print(table[0])

cur.close()
conn.close()