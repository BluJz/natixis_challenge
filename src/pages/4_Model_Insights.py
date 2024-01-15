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
    """, unsafe_allow_html=True,
    )


def get_and_display_column_names():
    """Get and displays the columns available in the src/models.mlruns database when called directly in the streamlit app."""
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


def get_and_display_sidebar():
    """Gets and displays in the form of a sidebar to select the models in the mlruns database directly in the streamlit app."""
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

    # Sidebar with model selection
    st.sidebar.header("Select a model: ")
    models = models_data
    if models:
        selected_model = st.sidebar.selectbox(
            "Available Models", models, format_func=lambda x: x[3]
        )
    else:
        st.sidebar.write("No available models.")

    # Close the database connection
    conn.close()

    return selected_model[0], selected_model[3]


def get_and_display_documentation(selected_model_name):
    # Create a dictionary to map model names to Wikipedia URLs
    model_wikipedia_links = {
        "Random Forest Regressor": "https://en.wikipedia.org/wiki/Random_forest",
        "Decision Tree Regressor": "https://en.wikipedia.org/wiki/Decision_tree_learning",
        "XGBoost Regressor": "https://en.wikipedia.org/wiki/XGBoost",
        "Linear Regression": "https://en.wikipedia.org/wiki/Linear_regression",
    }

    # Display the selected model's Wikipedia link
    if selected_model_name in model_wikipedia_links:
        wikipedia_url = model_wikipedia_links[selected_model_name]
        st.markdown(f"**[Documentation for {selected_model_name}]({wikipedia_url})**")
    else:
        st.write("There is no available documentation for the moment.")


def display_progress_bar(title, progress_value):
    progress_value_percentage = int(progress_value * 100)
    # Set a custom CSS style for the progress bar
    progress_bar_style = (
        f"background: linear-gradient(90deg, #F5BBF4 {progress_value_percentage}%, transparent {progress_value_percentage}%);"
        "border-radius: 5px;"
        "height: 30px;"
        "position: relative;"  # Add position for overlaying text
        "box-shadow: 0px 0px 0px 1px #F5BBF4 inset;"  # Add a border of the same color
    )

    # Display the title and styled progress bar
    st.write(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='{progress_bar_style}'>"
        f"<span style='color: black; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);'>{progress_value_percentage}%</span>"
        "</div>",
        unsafe_allow_html=True,
    )


def get_and_display_params(selected_model_id):
    # Connect to the 'mlruns.db' database
    conn = sqlite3.connect("src/models/mlruns.db")
    cursor = conn.cursor()

    # Query the parameters for the selected run
    cursor.execute(
        f"""
        SELECT key AS Parameter, value AS Value
        FROM params
        WHERE run_uuid = '{selected_model_id}'
    """
    )
    parameters_data = cursor.fetchall()

    # Check if parameters were found for the selected run
    if not parameters_data:
        st.write(f"No parameters found for run with run_uuid: {selected_model_id}")
    else:
        # Create a DataFrame from the retrieved parameters data
        parameters_df = pd.DataFrame(parameters_data, columns=["Parameter", "Value"])

        subheader_style = """
            <style>
            .custom-subheader {
                font-size: 20px;  /* Adjust the font size as needed */
                color: #F5BBF4;  /* Change the color to your desired value */
            }
            </style>   
        """
        # Display the parameters in a table
        st.write(subheader_style, unsafe_allow_html=True)
        st.markdown(
            "<p class='custom-subheader'>Parameters for Selected Run</p>",
            unsafe_allow_html=True,
        )

        # Apply custom CSS to center-align the table
        table_style = """
            <style>
                .center-table {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        """
        st.write(table_style, unsafe_allow_html=True)
        st.write(
            f"<div class='center-table'>{parameters_df.to_html(index=False)}</div>",
            unsafe_allow_html=True,
        )

        st.write("#")

    # Close the database connection
    conn.close()


def main_display_model_insights(selected_model_id, selected_model_name):
    set_header_color()
    st.title(f"Model insights: {selected_model_name}")

    # Horizontal separator
    st.markdown("<hr>", unsafe_allow_html=True)

    get_and_display_params(selected_model_id)

    get_and_display_documentation(selected_model_name)

    # Horizontal separator
    st.markdown("<hr>", unsafe_allow_html=True)


# Run the page function
if __name__ == "__main__":
    # get_and_display_column_names()
    # mlflow_db_button = st.button("Visualize updated database: ", key="mlflow_db_viz")
    # if mlflow_db_button:
    #     get_and_display_mlruns()

    selected_model_id, selected_model_name = get_and_display_sidebar()

    main_display_model_insights(selected_model_id, selected_model_name)

    display_progress_bar("Training accuracy metric", 0.56)
