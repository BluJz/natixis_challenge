import streamlit as st
import sqlite3
from sqlalchemy import create_engine
from models_feedback_sql import Feedback
from sqlalchemy.orm import sessionmaker

# Assumptions:
# - Models we build are saved in folders inside the 'models' folder with the following structure:
# my_model/
# │
# ├── MLmodel
# │
# ├── model/
# │   ├── model.pkl (or other format depending on the flavor)
# │
# ├── conda.yaml (optional)
# │
# └── requirements.txt (optional)

# - We create an SQL table to have feedback over the models


def set_header_color():
    st.markdown(
        """
        <style>
        h1, h2, h3, h4, h5, h6 {
            color: #5F259F; /* Violet Pantone color */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page3():
    feedback_db_uri = "sqlite:///src/models/feedback.db"
    engine = create_engine(feedback_db_uri)

    set_header_color()
    st.title("Model used for recommenders and clustering")

    # Streamlit interface to collect user feedback
    model_name = st.text_input("Model used")
    bond_issuer_name = st.text_input("Client name")
    amount = st.number_input("Amount")
    acceptation_status = st.checkbox("Accept (if not checked: Declined)")

    if st.button("Submit Feedback"):
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Assuming you have collected the relevant feedback information
            feedback_entry = Feedback(
                model_name=model_name,
                bond_issuer_name=bond_issuer_name,
                amount=amount,
                acceptation_status=acceptation_status,
            )

            # Add the feedback to the database
            session.add(feedback_entry)
            # Commit the transaction to save the new feedback entry to the database
            session.commit()
        st.success("Feedback submitted successfully")


if __name__ == "__main__":
    page3()
