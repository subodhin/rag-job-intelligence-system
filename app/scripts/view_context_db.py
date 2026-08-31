import sqlite3

DATABASE_PATH = "data/context.db"


connection = sqlite3.connect(
    DATABASE_PATH,
    timeout=10
)

cursor = connection.cursor()


cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""")

tables = [row[0] for row in cursor.fetchall()]


for table in tables:

    print("\n" + "=" * 70)
    print("TABLE:", table)
    print("=" * 70)

    cursor.execute("SELECT * FROM {}".format(table))

    rows = cursor.fetchall()

    cursor.execute("PRAGMA table_info({})".format(table))

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    print("Columns:")
    print(columns)

    print("\nRows:")

    if not rows:
        print("(empty)")
    else:
        for row in rows:
            print(row)


connection.close()