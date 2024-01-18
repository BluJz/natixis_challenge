import streamlit as st
from sql_querier import sql_querier
import pandas as pd
from datetime import date
from model_pipeline import (
    global_run,
    recommender_isin_code,
    recommender_isin_features,
)
from sqlalchemy import create_engine
from models_feedback_sql import Feedback
from sqlalchemy.orm import sessionmaker


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


# Placeholder functions for backend logic
def get_isin_statistics(isin_code):
    query = f"""SELECT 
    (SELECT SUM(Total_Traded_Volume) FROM ma_table WHERE ISIN = "{isin_code}") AS Total_Volume,
    sub.MidPrice,
    sub.Rating_Moodys AS Risk
    FROM 
    (SELECT MidPrice, Rating_Moodys, Deal_Date
    FROM ma_table
    WHERE ISIN = "{isin_code}"
    ORDER BY Deal_Date DESC
    LIMIT 1) sub;"""
    return sql_querier(query)


def get_company_recommendations(isin_code):
    # Replace with actual logic to get company recommendations
    return [
        ("Company A", "Strong growth"),
        ("Company B", "Stable market leader"),
        ("Company C", "Innovative startup"),
    ]


def get_company_statistics(company_name):
    # Replace with actual logic to fetch company statistics
    return {"Revenue": "200M", "Employees": "1000"}


def isin_features_form():
    # Create a dictionary to store bond information
    bond_info = {
        "ISIN": "NEW",
        "Coupon": 0.5,
        "BloomIndustrySubGroup": "",
        "Classification": "",
        "Country": "",
        "Ccy": "",
        "Rating_SP": "",
        "Deal_Date": date.today(),
        "Maturity": date.today(),
        "Type": "Fixed",
    }

    st.write("Enter New Bond Information:")

    # Create input fields for bond information
    bond_info["ISIN"] = st.text_input("ISIN", bond_info["ISIN"])
    bond_info["Coupon"] = st.number_input("Coupon", bond_info["Coupon"])
    bond_info["BloomIndustrySubGroup"] = st.text_input(
        "Bloom Industry SubGroup", bond_info["BloomIndustrySubGroup"]
    )
    bond_info["Classification"] = st.text_input(
        "Classification", bond_info["Classification"]
    )
    bond_info["Country"] = st.text_input("Country", bond_info["Country"])
    bond_info["Ccy"] = st.text_input("Currency", bond_info["Ccy"])
    bond_info["Rating_SP"] = st.text_input("Rating (S&P)", bond_info["Rating_SP"])
    bond_info["Deal_Date"] = st.date_input("Deal Date", bond_info["Deal_Date"])
    bond_info["Maturity"] = st.date_input("Maturity Date", bond_info["Maturity"])

    bond_types = ["Fixed", "Floating", "Convertible", "Other"]
    bond_info["Type"] = st.selectbox("Bond Type", bond_types)
    return bond_info


def isin_code_form():
    isin_code = st.text_input("Enter ISIN Code")
    return isin_code


def main():
    set_header_color()

    rqf_path = "RFQ_Data_Challenge_HEC.csv"
    (
        isin_to_features_dict,
        client_apetite_dict_hist,
        client_apetite_dict_recent,
        features,
        df_unique,
        similarity_matrix,
        scaler,
        one_hot_encoder,
        df,
        model_hash,
    ) = global_run(file_path=rqf_path)

    isin_code = None
    isin_features = None
    client_hist_new_bond = None
    client_recent_new_bond = None
    bonds_new_bond = None

    if "show_isin_code_form" not in st.session_state:
        st.session_state.show_isin_code_form = False
    if "show_isin_features_form" not in st.session_state:
        st.session_state.show_isin_features_form = False
    if "result_mode" not in st.session_state:
        st.session_state.result_mode = False

    st.title("ISIN-Based Company Recommender")
    st.write(
        "Enter an ISIN code or fill an ISIN features form and get recommended companies"
    )

    # Layout: Two columns
    col1, col2 = st.columns(2)

    with col1:
        submit_new_isin_code_button = st.button(
            "Submit new ISIN code (only)", key="submit_new_isin_code"
        )
    with col2:
        submit_new_isin_features_button = st.button(
            "Submit new ISIN features", key="submit_new_isin_features"
        )

    if submit_new_isin_features_button:
        if not st.session_state.result_mode:
            st.session_state.show_isin_features_form = True
            st.session_state.show_isin_code_form = False
    elif submit_new_isin_code_button:
        if not st.session_state.result_mode:
            st.session_state.show_isin_code_form = True
            st.session_state.show_isin_features_form = False

    if not st.session_state.result_mode:
        if st.session_state.show_isin_features_form:
            st.subheader("Enter ISIN new bond features: ")
            isin_features = isin_features_form()
            submit_isin_features_button = st.button(
                "Submit", key="submit_isin_features"
            )

            if submit_isin_features_button:
                st.success("ISIN features submitted")

                (
                    client_hist_new_bond,
                    client_recent_new_bond,
                    bonds_new_bond,
                ) = recommender_isin_features(
                    isin_features=isin_features,
                    scaler=scaler,
                    one_hot_encoder=one_hot_encoder,
                    client_apetite_dict_hist=client_apetite_dict_hist,
                    client_apetite_dict_recent=client_apetite_dict_recent,
                    features=features,
                    df_unique=df_unique,
                    n=3,
                )

                st.session_state.show_isin_features_form = False
                st.session_state.result_mode = True

        if st.session_state.show_isin_code_form:
            st.subheader("Enter ISIN code: ")
            isin_code = isin_code_form()
            submit_isin_code_button = st.button("Submit", key="submit_isin_code")

            if submit_isin_code_button:
                st.success("ISIN code submitted")

                (
                    client_hist_new_bond,
                    client_recent_new_bond,
                    bonds_new_bond,
                ) = recommender_isin_code(
                    isin_code=isin_code,
                    isin_to_features_dict=isin_to_features_dict,
                    client_apetite_dict_hist=client_apetite_dict_hist,
                    client_apetite_dict_recent=client_apetite_dict_recent,
                    features=features,
                    df_unique=df_unique,
                    n=3,
                )

                st.session_state.show_isin_code_form = False
                st.session_state.result_mode = True

    if st.session_state.result_mode:
        st.session_state.show_isin_code_form = False
        st.session_state.show_isin_features_form = False
        # Column 1: ISIN Input and Statistics
        with col1:
            st.subheader("ISIN Code Statistics: ")
            isin_stats = get_isin_statistics(isin_code)
            if isin_stats is not None:
                donnees = []
                for item in isin_stats:
                    donnees += [item]
                df_isin_stats = pd.DataFrame(
                    donnees, columns=["Total Traded Volume", "Mid Price($)", "Rating"]
                )
                st.table(df_isin_stats)
            else:
                st.write("Not available")

            st.subheader("Most similar bonds: ")
            st.dataframe(bonds_new_bond)

            if isin_code is not None:
                add_isin_code_feedback(
                    isin_code=isin_code,
                    model_hash=model_hash,
                    recommandations=client_recent_new_bond,
                )
            elif isin_features is not None:
                add_isin_features_feedback(
                    isin_features=isin_features,
                    model_hash=model_hash,
                    recommandations=client_recent_new_bond,
                )

        # Column 2: Company Recommendations and Statistics
        with col2:
            st.subheader("Recommended Companies for ISIN:", isin_code)
            if client_recent_new_bond is not None:
                for company in client_recent_new_bond:
                    st.write(f"Company: {company}")
                    # company_stats = get_company_statistics(company)  # TODO
                    # st.write("Company Statistics:")
                    # for key, value in company_stats.items():
                    #     st.write(f"{key}: {value}")
                    # st.write("---")

        reset_button = st.button("Reset", key="reset_button")
        if reset_button:
            st.session_state.result_mode = False


def add_isin_code_feedback(isin_code, model_hash, recommandations):
    """From a combination of request / result, displays a prefilled button to add feedback of the model specific model.

    Args:
        request (String): ISIN code
        result (List): Results given
        model_id (String): Identifier of the model for the feedback table
    """
    feedback_db_uri = "sqlite:///src/models/feedback.db"
    engine = create_engine(feedback_db_uri)

    if type(recommandations) is list:
        formatted_recommandation = [
            f"{i + 1} - {item}" for i, item in enumerate(recommandations)
        ]
        formatted_recommandation = "; ".join(formatted_recommandation)
    else:
        formatted_recommandation = recommandations

    accept_button = st.button("Accept recommandation", key="accept_isin_feedback")
    deny_button = st.button("Deny recommandation", key="deny_isin_feedback")

    if accept_button:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Assuming you have collected the relevant feedback information
            feedback_entry = Feedback(
                model_hash=model_hash,
                isin_code=isin_code,
                isin_features=None,
                company_name=formatted_recommandation,
                recommender_type="ISIN code to client",
                acceptation_status="Accepted",
            )

            # Add the feedback to the database
            session.add(feedback_entry)
            # Commit the transaction to save the new feedback entry to the database
            session.commit()

        st.success("Feedback added - Accepted recommandation !")
    elif deny_button:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Assuming you have collected the relevant feedback information
            feedback_entry = Feedback(
                model_hash=model_hash,
                isin_code=isin_code,
                isin_features=None,
                company_name=formatted_recommandation,
                recommender_type="ISIN code to client",
                acceptation_status="Denied",
            )

            # Add the feedback to the database
            session.add(feedback_entry)
            # Commit the transaction to save the new feedback entry to the database
            session.commit()
        st.success("Feedback added - Denied recommandation !")


def add_isin_features_feedback(isin_features, model_hash, recommandations):
    """From a combination of request / result, displays a prefilled button to add feedback of the model specific model.

    Args:
        request (String): ISIN code
        result (List): Results given
        model_id (String): Identifier of the model for the feedback table
    """
    feedback_db_uri = "sqlite:///src/models/feedback.db"
    engine = create_engine(feedback_db_uri)

    if type(isin_features) is dict:
        # Create the formatted string
        formatted_string = ""
        for key, value in isin_features.items():
            formatted_string += f"{key}: {value}; "

        # Remove the trailing space and semicolon
        formatted_string = formatted_string.strip("; ")

    if type(recommandations) is list:
        formatted_recommandation = [
            f"{i + 1} - {item}" for i, item in enumerate(recommandations)
        ]
        formatted_recommandation = "; ".join(formatted_recommandation)
    else:
        formatted_recommandation = recommandations

    accept_button = st.button("Accept recommandation", key="accept_isin_feedback")
    deny_button = st.button("Deny recommandation", key="deny_isin_feedback")

    if accept_button:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Assuming you have collected the relevant feedback information
            feedback_entry = Feedback(
                model_hash=model_hash,
                isin_code=None,
                isin_features=formatted_string,
                company_name=formatted_recommandation,
                recommender_type="ISIN features to client",
                acceptation_status="Accepted",
            )

            # Add the feedback to the database
            session.add(feedback_entry)
            # Commit the transaction to save the new feedback entry to the database
            session.commit()

        st.success("Feedback added - Accepted recommandation !")
    elif deny_button:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Assuming you have collected the relevant feedback information
            feedback_entry = Feedback(
                model_hash=model_hash,
                isin_code=None,
                isin_features=formatted_string,
                company_name=formatted_recommandation,
                recommender_type="ISIN features to client",
                acceptation_status="Denied",
            )

            # Add the feedback to the database
            session.add(feedback_entry)
            # Commit the transaction to save the new feedback entry to the database
            session.commit()
        st.success("Feedback added - Denied recommandation !")


# Run the page function
if __name__ == "__main__":
    # Problems: the 'Submitted' form is still displayed after submitting the button
    main()
