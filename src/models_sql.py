import sqlite3

conn = sqlite3.connect("feedback.db")  # Create or connect to a SQLite database file

# Create a table to store user feedback
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_feedback (
        user_id INTEGER PRIMARY KEY,
        model_name TEXT,
        recommendation_status BOOLEAN,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
)
conn.commit()
