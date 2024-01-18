import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from models_feedback_sql import Feedback

# from test import test_function
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
    h1 {
        color: #F5BBF4;
    }
    h2 {
        color: #F5BBF4;
    }
    h3 {
        color: #B981EC;
    }
    h4 {
        color: #B981EC;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    feedback_db_uri = "sqlite:///src/models/feedback.db"
    engine = create_engine(feedback_db_uri)

    set_header_color()

    update_viz_feedback_button = st.button(
        "Visualize updated database: ", key="updateviz_feedback"
    )

    if update_viz_feedback_button:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Query the database to retrieve feedback data
            feedback_data = session.query(Feedback).all()

            feedback_df = pd.DataFrame(
                [
                    (
                        f.id,
                        f.model_hash,
                        f.isin_code,
                        f.isin_features,
                        f.company_name,
                        f.recommender_type,
                        f.acceptation_status,
                    )
                    for f in feedback_data
                ],
                columns=[
                    "ID",
                    "Model hash",
                    "ISIN Code",
                    "ISIN features",
                    "Company name",
                    "Recommender type",
                    "Acceptation Status",
                ],
            )
        st.table(feedback_df)


if __name__ == "__main__":
    main()
