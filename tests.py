import sqlite3


def check_relationships(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Table Relationships in the Database:\n")

    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

        # Check foreign keys for the table
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys = cursor.fetchall()

        if foreign_keys:
            for fk in foreign_keys:
                print(f"  Foreign Key: {fk[3]} -> {fk[2]}({fk[4]})")
        else:
            print("  No foreign keys.")

        print()

    connection.close()


# Replace 'your_database.db' with the path to your SQLite database file
check_relationships('app/db/app.db')
