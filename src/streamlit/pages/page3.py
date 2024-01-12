import streamlit as st
import sqlite3

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
    st.markdown("""
        <style>
        h1, h2, h3, h4, h5, h6 {
            color: #5F259F; /* Violet Pantone color */
        }
        </style>
        """, unsafe_allow_html=True)

def page3():
    set_header_color()
    st.title("Model used for recommenders and clustering")

    # Create a connection to the SQLite database
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()

    # Streamlit interface to collect user feedback
    user_id = st.text_input("User ID")
    model_name = st.text_input("Model Name")
    recommendation_status = st.checkbox("Used Recommended Clients")

    if st.button("Submit Feedback"):
        # Insert user feedback into the database
        cursor.execute(
            """
            INSERT INTO user_feedback (user_id, model_name, recommendation_status)
            VALUES (?, ?, ?)
        """,
            (user_id, model_name, recommendation_status),
        )
        conn.commit()
        st.success("Feedback submitted successfully")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    page3()
