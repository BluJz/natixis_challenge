import sqlite3
import os

def sql_querier(query):
    # Get the absolute path to the database file
    db_file_path = os.path.abspath("src/stats/stats.db")

    # Create or connect to the SQLite database
    print(db_file_path)
    conn = sqlite3.connect(db_file_path)

    cursor = conn.cursor()

    # SQL query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    for row in results:
        print(row)

    cursor.close()
    conn.close()
