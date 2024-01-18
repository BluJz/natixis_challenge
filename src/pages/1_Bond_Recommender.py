import streamlit as st
from sql_querier import sql_querier
import pandas as pd
from sqlalchemy import create_engine
from models_feedback_sql import Feedback
from model_pipeline import global_run, recommender_client
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
def get_company_statistics(company_short_name):
    query = f"""SELECT 
    ISIN, 
    Rating_Moodys AS Risk, 
    B_price * Total_Requested_Volume AS "Amount traded"
    FROM ma_table
    WHERE ma_table.company_short_name = "{company_short_name}"
    ORDER BY Deal_Date DESC
    LIMIT 3;"""
    return sql_querier(query)


def get_bond_statistics(bond_name):
    # Replace with actual logic to fetch bond statistics
    return {"Yield": "5%", "Rating": "AAA"}


def set_result_mode(company_short_name):
    st.session_state.bond_recommender_company_short_name = company_short_name
    st.session_state.show_client_form = False
    st.session_state.result_mode_client = True


def set_form_mode():
    print("callback")
    st.session_state.bond_recommender_company_short_name = None
    st.session_state.show_client_form = True
    st.session_state.result_mode_client = False


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

    if "show_client_form" not in st.session_state:
        st.session_state.show_client_form = True
    if "result_mode_client" not in st.session_state:
        st.session_state.result_mode_client = False
    if "bond_recommender_company_short_name" not in st.session_state:
        st.session_state.bond_recommender_company_short_name = None
    company_short_name = None

    placeholder = st.empty()

    if st.session_state.show_client_form:
        with placeholder.container():
            st.title("Company Bond Recommender")
            st.write(
                "Enter the name of a company and get the most recommended bonds for this client"
            )

            company_short_name = st.text_input(
                "Enter Company Short Name (Don't forget to press Enter once finished!)"
            )
            run_button = st.button(
                "Run Recommender",
                on_click=set_result_mode,
                args=[company_short_name],
                key="company_to_isin_recommender",
            )

    if st.session_state.result_mode_client:
        with placeholder.container():
            # Layout: Two columns
            col1, col2 = st.columns(2)

            company_stats = get_company_statistics(
                st.session_state.bond_recommender_company_short_name
            )
            client_hist_apetite, top_n_bonds = recommender_client(
                client_name=st.session_state.bond_recommender_company_short_name,
                df=df,
                isin_to_features_dict=isin_to_features_dict,
                features=features,
                df_unique=df_unique,
                n=3,
            )

            # Column 1: Company Search and Statistics
            with col1:
                if company_stats is not None:
                    donnees = []
                    for item in company_stats:
                        donnees += [item]
                    df_bond_stats = pd.DataFrame(
                        donnees, columns=["ISIN", "Rating", "Montant($)"]
                    )
                    st.subheader(
                        f"3 most recent {st.session_state.bond_recommender_company_short_name} transactions:"
                    )
                    st.table(df_bond_stats)
                else:
                    st.write("Not available")

                feedback_recommandations = list(top_n_bonds.ISIN)
                add_client_feedback(
                    client_name=st.session_state.bond_recommender_company_short_name,
                    model_hash=model_hash,
                    recommandations=feedback_recommandations,
                )

            # Column 2: Bond Recommendations and Statistics
            with col2:
                st.subheader(
                    f"Recommended Bonds for: {st.session_state.bond_recommender_company_short_name}"
                )
                st.dataframe(top_n_bonds)

            reset_button = st.button(
                "Reset", on_click=set_form_mode, key="reset_button"
            )


def add_client_feedback(client_name, model_hash, recommandations):
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

    # st.write(client_name)

    if accept_button:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Assuming you have collected the relevant feedback information
            feedback_entry = Feedback(
                model_hash=model_hash,
                isin_code=formatted_recommandation,
                isin_features=None,
                company_name=client_name,
                recommender_type="Client to bond",
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
                isin_code=formatted_recommandation,
                isin_features=None,
                company_name=client_name,
                recommender_type="Client to bond",
                acceptation_status="Denied",
            )

            # Add the feedback to the database
            session.add(feedback_entry)
            # Commit the transaction to save the new feedback entry to the database
            session.commit()
        st.success("Feedback added - Denied recommandation !")


# Run the page function
if __name__ == "__main__":
    # Problems: have to click twice on the reset button
    main()
