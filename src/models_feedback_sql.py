from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import random
from faker import Faker
import os

# Create a SQLAlchemy engine and session
engine = create_engine(
    "sqlite:///src/models/feedback.db"
)  # Use a different database name
Session = sessionmaker(bind=engine)
session = Session()

# Create a declarative base
Base = declarative_base()


# Define a Feedback table
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)  # Add an 'id' column as the primary key
    model_hash = Column(String)
    isin_code = Column(String)
    isin_features = Column(String)
    company_name = Column(String)
    recommender_type = Column(String)
    acceptation_status = Column(String)


# Create the table (if it doesn't exist)
Base.metadata.create_all(engine)
