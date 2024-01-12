import sqlite3
import os

# Get the absolute path to the database file
db_file_path = os.path.abspath("src/stats/stats.db")

# Create or connect to the SQLite database
print(db_file_path)
conn = sqlite3.connect(db_file_path)
conn.close()

# Create a table to store user feedback
# cursor = conn.cursor()
# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS user_feedback (
#         user_id INTEGER PRIMARY KEY,
#         model_name TEXT,
#         recommendation_status BOOLEAN,
#         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# """
# )
# conn.commit()