from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import random
from faker import Faker
import os

# Create a SQLAlchemy engine and session
engine = create_engine(
    "sqlite:///src/models/models.db"
)  # Use a different database name
Session = sessionmaker(bind=engine)
session = Session()

# Create a declarative base
Base = declarative_base()


# Define a Feedback table
# class Feedback(Base):
#     __tablename__ = "feedback"
#     id = Column(Integer, primary_key=True)  # Add an 'id' column as the primary key
#     model_hash = Column(String)
#     isin_code = Column(String)
#     isin_features = Column(String)
#     company_name = Column(String)
#     recommender_type = Column(String)
#     acceptation_status = Column(String)


class Models(Base):
    __tablename__ = "models"
    model_hash = Column(String, primary_key=True)
    model_name = Column(String)
    model_description = Column(String)
    model_parameters = Column(String)


# Create the table (if it doesn't exist)
Base.metadata.create_all(engine)

# # Create a SQLite database (fake_feedback.db)
# conn = sqlite3.connect("src/models/fake_feedback.db")
# cursor = conn.cursor()

# # Create a 'feedback' table
# cursor.execute(
#     """
#     CREATE TABLE feedback (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         run_uuid TEXT,
#         amount REAL,
#         acception_status INTEGER
#     )
# """
# )

# # Generate fake feedback data for the specified run_uuid values
# fake = Faker()
# run_uuids = [
#     "2b11c737da0f434c82059108d0e7f5d7",
#     "257fc294fc9b48c98bc175a33e800d83",
#     "15ff4a8eb8e74ad8a9eead742fe26e87",
#     "a8a1959074ce4ad188c0b5116b42a2da",
# ]

# for _ in range(100):  # Generate 100 fake feedback records
#     run_uuid = random.choice(run_uuids)
#     amount = random.uniform(1, 100)
#     acception_status = random.choice([0, 1])

#     cursor.execute(
#         """
#         INSERT INTO feedback (run_uuid, amount, acception_status)
#         VALUES (?, ?, ?)
#     """,
#         (run_uuid, amount, acception_status),
#     )

# # Commit the changes and close the database
# conn.commit()
# conn.close()
