import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database import get_connection


conn = get_connection()
cur = conn.cursor()

query = """
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name = 'orders'
ORDER BY ordinal_position;
"""

cur.execute(query)

columns = cur.fetchall()

print("=" * 60)
print("OPSLENS AI - ORDERS TABLE SCHEMA")
print("=" * 60)

for column, data_type in columns:
    print(f"{column:<35} {data_type}")

cur.close()
conn.close()
