import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from models_feedback_sql import Feedback
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from PIL import Image
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


def get_and_display_column_names():
    # Connect to the MLflow tracking server
    mlflow.set_tracking_uri("sqlite:///src/models/mlruns.db")

    # Streamlit UI layout
    st.title("Columns in mlruns.db Database")

    # Get all registered experiments
    experiments = mlflow.search_runs()
    if not experiments.empty:
        st.subheader("Columns in 'experiments' Table:")
        st.write(experiments.columns.tolist())
    else:
        st.write("No data found in 'experiments' table.")

    # Close the database connection
    mlflow.end_run()


def get_and_display_mlruns():
    # Connect to the 'mlruns.db' database
    conn = sqlite3.connect("src/models/mlruns.db")
    cursor = conn.cursor()

    # Specify the SQL query to retrieve the "save_model_for_usage" tag and other columns
    sql_query = """
    SELECT 
        runs.run_uuid, 
        runs.end_time, 
        tags.key AS tag_key, 
        tags.value AS tag_value
    FROM runs
    LEFT JOIN tags ON runs.run_uuid = tags.run_uuid
    WHERE tags.key = 'save_model_for_usage'
    """

    # Execute the query and fetch the results into a DataFrame
    runs_with_save_tag = pd.read_sql_query(sql_query, conn)

    # Define a CSS class to apply text wrapping to table cells
    table_style = """
    <style>
        .stDataFrame {
            white-space: normal;
        }
    </style>
    """

    # Display the runs with the "save_model_for_usage" tag in the Streamlit interface
    st.title('Runs with "save_model_for_usage" Tag')
    st.write(table_style, unsafe_allow_html=True)
    st.dataframe(runs_with_save_tag)

    # Close the database connection
    conn.close()


def get_and_display_all_models():
    # Connect to the 'mlruns.db' database
    conn = sqlite3.connect("src/models/mlruns.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT DISTINCT runs.run_uuid, runs.end_time, tags.value, params.value AS model_name
    FROM runs
    LEFT JOIN tags ON runs.run_uuid = tags.run_uuid
    LEFT JOIN params ON runs.run_uuid = params.run_uuid
    WHERE tags.key = 'save_model_for_usage' AND tags.value = 'true' AND params.key = 'model_name'
    ORDER BY runs.end_time DESC
    """
    )
    models_data = cursor.fetchall()
    if not models_data:
        models_data = None

    # Streamlit UI layout
    st.title("Model Explorer")

    # Sidebar with model selection
    st.sidebar.header("Select a Model")
    models = models_data
    if models:
        selected_model = st.sidebar.selectbox(
            "Available Models", models, format_func=lambda x: x[3]
        )
    else:
        st.sidebar.write("No available models.")

    # Display information about the selected model
    if models:
        st.subheader("Selected Model Information")
        st.write(f"Model ID: {selected_model[0]}")
        st.write(f"End Time: {selected_model[1]}")
        # You can add more information about the selected model here

    # Close the database connection
    conn.close()


# Function to get unique model identifiers based on model name and training date
def get_unique_model_identifiers(mlruns_conn):
    cursor = mlruns_conn.cursor()
    cursor.execute("SELECT DISTINCT model_name, end_time FROM runs")
    models = cursor.fetchall()
    unique_identifiers = [f"{model[0]} - {model[1]}" for model in models]
    return unique_identifiers


# Function to get training metrics for a selected model
def get_training_metrics(selected_identifier, mlruns_conn):
    model_name, end_time = selected_identifier.split(" - ")
    cursor = mlruns_conn.cursor()
    cursor.execute(
        f"SELECT * FROM runs WHERE model_name = '{model_name}' AND end_time = '{end_time}'"
    )
    runs_data = cursor.fetchall()
    if runs_data:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(runs_data, columns=columns)
        return df[["accuracy", "loss"]]
    else:
        return None


# Function to get model architecture image and description
def get_model_info(selected_identifier):
    # You can customize this function to fetch the model architecture image and description
    # based on the selected model name from your own data source.
    model_description = "Random Forest with 100 estimators"  # Example description
    model_image = Image.open("model_architecture.png")  # Example image
    return model_description, model_image


# Function to get user feedback metrics
def get_user_feedback_metrics(selected_identifier, feedback_conn):
    model_name, _ = selected_identifier.split(" - ")
    cursor = feedback_conn.cursor()
    cursor.execute(f"SELECT * FROM feedback WHERE model_name = '{model_name}'")
    feedback_data = cursor.fetchall()
    if feedback_data:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(feedback_data, columns=columns)
        return df
    else:
        return None


def display_progress_bar(title, progress_value):
    progress_value_percentage = int(progress_value * 100)
    # Set a custom CSS style for the progress bar
    progress_bar_style = (
        f"background: linear-gradient(90deg, #82CAFF {progress_value_percentage}%, transparent {progress_value_percentage}%);"
        "border-radius: 5px;"
        "height: 30px;"
        "position: relative;"  # Add position for overlaying text
        "box-shadow: 0px 0px 0px 1px #82CAFF inset;"  # Add a border of the same color
    )

    # Display the title and styled progress bar
    st.write(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='{progress_bar_style}'>"
        f"<span style='color: black; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);'>{progress_value_percentage}%</span>"
        "</div>",
        unsafe_allow_html=True,
    )


def main_2():
    # Connect to the mlruns.db and feedback.db databases
    mlruns_conn = sqlite3.connect("mlruns.db")
    feedback_conn = sqlite3.connect("feedback.db")

    # Streamlit UI layout
    st.title("Model Explorer")

    # Model Selection Area (Upper Left)
    unique_identifiers = get_unique_model_identifiers(mlruns_conn)
    selected_identifier = st.sidebar.selectbox("Select a Model", unique_identifiers)

    # Training Metrics Area (Bottom Left)
    st.subheader("Training Metrics")
    metrics_df = get_training_metrics(selected_identifier, mlruns_conn)
    if metrics_df is not None:
        for metric in metrics_df.columns:
            st.write(f"{metric.capitalize()}:")
            st.progress(metrics_df[metric].iloc[-1])

    # Model Architecture Area (Upper Right)
    st.subheader("Model Architecture")
    model_description, model_image = get_model_info(selected_identifier)
    st.image(model_image, caption=model_description, use_column_width=True)

    # User Feedback Metrics Area (Bottom Right)
    st.subheader("User Feedback Metrics")
    feedback_metrics_df = get_user_feedback_metrics(selected_identifier, feedback_conn)
    if feedback_metrics_df is not None:
        st.write(feedback_metrics_df)

    # Close database connections
    mlruns_conn.close()
    feedback_conn.close()


# Run the page function
if __name__ == "__main__":
    get_and_display_column_names()
    mlflow_db_button = st.button("Visualize updated database: ", key="mlflow_db_viz")
    if mlflow_db_button:
        get_and_display_mlruns()
    get_and_display_all_models()

    display_progress_bar("Accuracy metric", 0.56)
