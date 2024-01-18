import streamlit as st
import pandas as pd
import sqlite3
import mlflow
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models_db_creation import Models
from models_feedback_sql import Feedback
from collections import Counter


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


def get_and_display_sidebar(session):
    """Gets and displays in the form of a sidebar to select the models in the mlruns database directly in the streamlit app."""
    # Connect to the 'models.db' database
    st.sidebar.title("Select a Model")

    # Retrieve the list of model names and model hashes from the database
    models = session.query(Models.model_name, Models.model_hash).all()
    model_names = [model[0] for model in models]
    model_hashes = {model[0]: model[1] for model in models}

    # Create a selectbox in the sidebar for model selection
    selected_model_name = st.sidebar.selectbox("Choose a Model", model_names)

    # Get the corresponding model_hash using the selected model name
    selected_model_hash = model_hashes.get(selected_model_name, None)

    return selected_model_hash


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


# Function to retrieve model description based on selected_model_hash
def get_model_name_and_description(selected_model_hash, session):
    # Query the database to get the model description for the selected model hash
    model = (
        session.query(Models).filter(Models.model_hash == selected_model_hash).first()
    )

    if model:
        return model.model_name, model.model_description
    else:
        return None, None


def get_feedback_details(selected_model_hash):
    # Create a SQLAlchemy engine and session
    engine_feedback = create_engine(
        "sqlite:///src/models/feedback.db"
    )  # Replace with your database file path
    Session_feedback = sessionmaker(bind=engine_feedback)
    session_feedback = Session_feedback()

    # Query the database to get feedback data for the selected model_hash
    feedback_data = (
        session_feedback.query(Feedback).filter_by(model_hash=selected_model_hash).all()
    )

    # Get the number of feedback entries for the selected model_hash
    num_feedback = len(feedback_data)

    # Calculate the percentage of feedback entries for the selected model_hash
    total_entries = session_feedback.query(Feedback).count()
    percentage = num_feedback / total_entries if total_entries > 0 else 0

    # Calculate the most represented category in 'recommender_type'
    recommender_types = [feedback.recommender_type for feedback in feedback_data]
    most_common_category = None
    if recommender_types:
        counter = Counter(recommender_types)
        most_common_category = counter.most_common(1)[0][0]

    # Close the session
    session_feedback.close()

    return num_feedback, percentage, most_common_category


def display_feedback(num_feedback, percentage, most_common_category):
    # Display feedback summary
    if num_feedback > 0:
        st.subheader("Feedback Summary")

        # Create a layout for the table with centered text in each cell
        kpi_table_layout = """
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    text-align: center;
                    padding: 10px;
                }}
            </style>
            <table>
                <tr>
                    <th>Number of feedbacks</th>
                    <th>Percentage of feedback entries</th>
                    <th>Most common recommender type</th>
                </tr>
                <tr>
                    <td>{}</td>
                    <td>{:.1f}</td>
                    <td>{}</td>
                </tr>
            </table>
        """.format(
            int(num_feedback), percentage, most_common_category
        )

        # Display the table layout using st.markdown
        st.markdown(kpi_table_layout, unsafe_allow_html=True)

    else:
        st.warning("No feedback data found for the specified hash model.")


def calculate_accepted_percentage(selected_model_hash):
    # Create a SQLAlchemy engine and session
    engine_feedback = create_engine(
        "sqlite:///src/models/feedback.db"
    )  # Replace with your database file path
    Session_feedback = sessionmaker(bind=engine_feedback)
    session_feedback = Session_feedback()

    # Query the database to count the number of accepted recommendations
    total_count = (
        session_feedback.query(Feedback)
        .filter_by(model_hash=selected_model_hash)
        .count()
    )
    accepted_count = (
        session_feedback.query(Feedback)
        .filter_by(model_hash=selected_model_hash, acceptation_status="Accepted")
        .count()
    )

    # Calculate the percentage
    if total_count > 0:
        percentage = accepted_count / total_count
    else:
        percentage = 0.0

    # Close the session
    session_feedback.close()

    return percentage


def set_add_model_mode():
    st.session_state.add_model_mode = True
    st.session_state.model_insights_mode = False


def add_model_form():
    st.header("Adding model form")
    # Create a dictionary to store bond information
    model_info = {
        "model_hash": "NEW",
        "model_name": "",
        "model_description": "",
        "model_parameters": "",
    }

    st.write("Enter New Model Information: (Don't forget to press enter!)")

    # Create input fields for bond information
    model_info["model_hash"] = st.text_input("Model hash: ", model_info["model_hash"])
    model_info["model_name"] = st.text_input("Model name: ", model_info["model_name"])
    model_info["model_description"] = st.text_input(
        "Model description: ", model_info["model_description"]
    )
    model_info["model_parameters"] = st.text_input(
        "Model parameters: ", model_info["model_parameters"]
    )

    return model_info


def add_model_to_db(model_info):
    feedback_db_uri = "sqlite:///src/models/models.db"
    engine = create_engine(feedback_db_uri)

    if model_info is not None:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            models_entry = Models(
                model_hash=model_info["model_hash"],
                model_name=model_info["model_name"],
                model_description=model_info["model_description"],
                model_parameters=model_info["model_parameters"],
            )

            session.add(models_entry)
            session.commit()

        # st.success("Model added !")

    st.session_state.add_model_mode = False
    st.session_state.model_insights_mode = True


def main():
    if "model_insights_mode" not in st.session_state:
        st.session_state.model_insights_mode = True
    if "add_model_mode" not in st.session_state:
        st.session_state.add_model_mode = False

    # Create a SQLAlchemy engine and session
    engine = create_engine(
        "sqlite:///src/models/models.db"
    )  # Replace with your database URL
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a declarative base
    # Base = declarative_base()

    placeholder = st.empty()

    if st.session_state.model_insights_mode:
        with placeholder.container():
            st.subheader("Feel free to add a model: ")
            add_model_button = st.button(
                "Add model", on_click=set_add_model_mode, key="set_add_model_mode"
            )

            selected_model_hash = get_and_display_sidebar(session=session)
            if selected_model_hash:
                model_name, model_description = get_model_name_and_description(
                    selected_model_hash, session=session
                )
                if model_name and model_description:
                    st.header(model_name)
                    st.write(model_description)

                    st.divider()

                    feedback_acception_percentage = calculate_accepted_percentage(
                        selected_model_hash
                    )
                    display_progress_bar(
                        title="Feedback acception percentage",
                        progress_value=feedback_acception_percentage,
                    )

                    st.divider()

                    (
                        num_feedback,
                        percentage,
                        most_common_category,
                    ) = get_feedback_details(selected_model_hash)
                    display_feedback(
                        num_feedback=num_feedback,
                        percentage=percentage,
                        most_common_category=most_common_category,
                    )

                else:
                    st.warning("Model not found.")
            else:
                st.write("No model selected.")

    if st.session_state.add_model_mode:
        with placeholder.container():
            model_info = add_model_form()

            submit_model_info_button = st.button(
                "Submit and add model",
                on_click=add_model_to_db,
                args=[model_info],
                key="submit_model_info_button",
            )


# Run the page function
if __name__ == "__main__":
    main()
