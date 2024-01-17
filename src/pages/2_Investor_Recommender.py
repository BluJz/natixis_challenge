import streamlit as st
from sql_querier import sql_querier
import pandas as pd


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
        "ISIN": "",
        "Coupon": 0.5,
        "BloomIndustrySubGroup": "",
        "Classification": "",
        "Country": "",
        "Ccy": "",
        "Rating_SP": "",
        "Deal_Date": "",
        "Maturity": "",
        "Type": "Fixed",
    }

    st.write("Enter New Bond Information:")

    # Create input fields for bond information
    # bond_info["ISIN"] = st.text_input("ISIN", bond_info["ISIN"])
    bond_info["ISIN"] = "NEW"
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
    bond_info["Type"] = st.selectbox(
        "Bond Type", ["Fixed", "Floating", "Convertible", "Other"], bond_info["Type"]
    )

    # Save the bond information when the "Submit" button is clicked
    submit_button = st.button("Submit", key="submit")
    if submit_button:
        st.success("Bond Information Submitted:")
        return bond_info


def isin_code_form():
    isin_code = st.text_input("Enter ISIN Code")
    # Save the bond information when the "Submit" button is clicked

    # if submit_button:
    #     return isin_code, True
    return isin_code


def main():
    set_header_color()
    st.title("ISIN-Based Company Recommender")
    st.write(
        "Enter an ISIN code or fill an ISIN features form and get recommended companies"
    )

    # Layout: Two columns
    col1, col2 = st.columns(2)

    # run_button = st.button("Run Recommender", key="isin_to_company_recommender")
    with col1:
        submit_new_isin_code_button = st.button(
            "Submit new ISIN code (only)", key="submit_new_isin_code"
        )
    with col2:
        submit_new_isin_features_button = st.button(
            "Submit new ISIN features", key="submit_new_isin_features"
        )

    # submit_isin_code_button = None
    # submit_isin_features_button = None
    # if submit_new_isin_features_button:
    #     isin_features = isin_features_form()
    #     submit_isin_features_button = st.button("Submit", key="submit_isin_features")
    # elif submit_new_isin_code_button:
    #     isin_code = isin_code_form()
    #     submit_isin_code_button = st.button("Submit", key="submit_isin_code")

    # if submit_isin_code_button:
    #     st.success("ISIN code submitted.")
    # elif submit_isin_features_button:
    #     st.success("ISIN features submitted.")

    # Initialize session state to manage form state
    if "show_code_form" not in st.session_state:
        st.session_state.show_code_form = False

    # Create the Streamlit app
    st.title("ISIN Code Submission")

    # Check if the "Enter new code" button is clicked
    if st.button("Enter new code"):
        st.session_state.show_code_form = True

    # Display the ISIN code input form if the flag is True
    if st.session_state.show_code_form:
        st.subheader("Enter ISIN code:")
        isin_code = st.text_input("ISIN Code:")
        submit_button = st.button("Submit")

        # Check if the "Submit" button is clicked
        if submit_button:
            # Process the ISIN code (e.g., validation or further actions)
            # Display a success message
            st.success("ISIN code submitted.")
            # Hide the form by setting the session state flag to False
            st.session_state.show_code_form = False

    # # Column 1: ISIN Input and Statistics
    # with col1:
    #     if run_button and isin_code:
    #         st.subheader("ISIN Code Statistics:")
    #         isin_stats = get_isin_statistics(isin_code)
    #         if isin_stats is not None:
    #             donnees = []
    #             for item in isin_stats:
    #                 donnees += [item]
    #             df = pd.DataFrame(
    #                 donnees, columns=["Total Traded Volume", "Mid Price($)", "Rating"]
    #             )
    #             st.table(df)
    #         else:
    #             st.write("Not available")

    # # Column 2: Company Recommendations and Statistics
    # with col2:
    #     if run_button and isin_code:
    #         st.subheader("Recommended Companies for ISIN:", isin_code)
    #         recommended_companies = get_company_recommendations(isin_code)

    #         for company, reason in recommended_companies:
    #             st.write(f"Company: {company}")
    #             st.write(f"Reason: {reason}")
    #             company_stats = get_company_statistics(company)
    #             st.write("Company Statistics:")
    #             for key, value in company_stats.items():
    #                 st.write(f"{key}: {value}")
    #             st.write("---")


# Run the page function
if __name__ == "__main__":
    main()
