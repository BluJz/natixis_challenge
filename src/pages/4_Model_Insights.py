import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from models_feedback_sql import Feedback
from sqlalchemy.orm import sessionmaker

import mlflow


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


# Placeholder functions for backend logic
def update_model():
    # Replace with actual logic to update the model in cache
    # This function should update the model and return the new model name and validation metric
    return "New Model Name", 0.95  # Example return values


def get_current_model_name():
    # Replace with actual logic to get the current model name
    return "Current Model Name"


def get_validation_metric(model_name):
    # Replace with actual logic to get the validation metric for the given model
    return 0.93  # Example return value


def page4():
    set_header_color()
    st.title("Models Insights")

    # Button to update the model
    if st.button("Update Model"):
        new_model_name, validation_metric = update_model()
        st.success(
            f"Model updated to {new_model_name} with validation metric score: {validation_metric}"
        )
    else:
        # Displaying current model information
        current_model_name = get_current_model_name()
        st.write(f"Current Model: {current_model_name}")
        validation_metric = get_validation_metric(current_model_name)
        st.write(f"Validation Metric Score: {validation_metric}")


def main():
    # models_db_uri = "sqlite:///src/models/models.db"
    # engine = create_engine(models_db_uri)

    # Set the tracking URI to your mlruns.db file
    mlflow.set_tracking_uri("sqlite:///src/models/mlruns.db")

    st.title("Models Insights")

    # if st.button("Visualize updated database: "):
    #     Session = sessionmaker(bind=engine)
    #     with Session() as session:
    #         # Query the database to retrieve feedback data
    #         models_data = session.query(Feedback).all()

    #         feedback_df = pd.DataFrame(
    #             [
    #                 (f.model_name, f.bond_issuer_name, f.amount, f.acceptation_status)
    #                 for f in feedback_data
    #             ],
    #             columns=[
    #                 "Model Name",
    #                 "Bond Issuer Name",
    #                 "Amount",
    #                 "Acceptation Status",
    #             ],
    #         )
    #     st.table(feedback_df)

    mlflow_db_button = st.button("Visualize updated database: ", key="mlflow_db_viz")
    if mlflow_db_button:
        # List all experiments available in the tracking database
        experiment_ids = mlflow.search_runs().experiment_id.unique()

        # Choose an experiment ID (you can choose the one you've been using)
        experiment_id = experiment_ids[0]

        # Query the runs within the chosen experiment
        # runs = mlflow.search_runs(experiment_ids=[experiment_id])
        runs = mlflow.search_runs(
            experiment_ids=[experiment_id], filter_string="", order_by=["end_time DESC"]
        )
        selected_columns = [
            "run_id",
            "end_time",
        ]  # Add the columns you're interested in here
        selected_columns += [
            col
            for col in runs.columns
            if col.startswith("params.") or col.startswith("metrics.")
        ]
        runs = runs[selected_columns]
        # Get the names of the columns in the DataFrame
        # column_names = runs.columns.tolist()

        # Define a CSS class to apply text wrapping to table cells
        table_style = """
        <style>
            .stDataFrame {
                white-space: normal;
            }
        </style>
        """

        # Display just the column names
        # st.write("Column Names:")
        # st.write(column_names)

        # Display the runs as a DataFrame
        st.write("MLflow Runs:")
        st.write(table_style, unsafe_allow_html=True)
        st.dataframe(runs)


# Run the page function
if __name__ == "__main__":
    main()
