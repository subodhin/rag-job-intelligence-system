from app.context.database import initialize_database, get_connection


initialize_database()

connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
""")

tables = cursor.fetchall()

print("Context database initialized.")
print("Tables:")

for table in tables:
    print("-", table[0])

connection.close()