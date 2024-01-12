from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String)
    bond_issuer_name = Column(String)
    amount = Column(Integer)
    acceptation_status = Column(String)


# Create the table (if it doesn't exist)
Base.metadata.create_all(engine)
