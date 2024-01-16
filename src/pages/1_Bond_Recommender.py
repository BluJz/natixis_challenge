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


def get_bond_recommendations(company_short_name):
    # Replace with actual logic to get bond recommendations
    return [
        ("Bond A", "High yield"),
        ("Bond B", "Stable investment"),
        ("Bond C", "Low risk"),
    ]


def get_bond_statistics(bond_name):
    # Replace with actual logic to fetch bond statistics
    return {"Yield": "5%", "Rating": "AAA"}


def bond_form():
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
    bond_info["Type"] = st.selectbox(
        "Bond Type", ["Fixed", "Floating", "Convertible", "Other"], bond_info["Type"]
    )

    # Save the bond information when the "Submit" button is clicked
    if st.button("Submit"):
        st.write("Bond Information Submitted:")
        st.write(bond_info)


def main():
    set_header_color()
    st.title("Company Bond Recommender")
    st.write(
        "Enter the name of a company and get the most recommended bonds for this client"
    )

    company_short_name = st.text_input("Enter Company Short Name")
    run_button = st.button("Run Recommender", key="company_to_isin_recommender")

    # Layout: Two columns
    col1, col2 = st.columns(2)

    # Column 1: Company Search and Statistics
    with col1:
        if run_button and company_short_name:
            company_stats = get_company_statistics(company_short_name)
            if company_stats is not None:
                donnees = []
                for item in company_stats:
                    donnees += [item]
                df = pd.DataFrame(donnees, columns=["ISIN", "Rating", "Montant($)"])
                st.subheader("3 most recent client transactions:")
                st.table(df)
            else:
                st.write("Not available")

    # Column 2: Bond Recommendations and Statistics
    with col2:
        if run_button and company_short_name:
            request_feedback("", "", "")
            st.subheader(f"Recommended Bonds for: {company_short_name}")
            recommended_bonds = get_bond_recommendations(company_short_name)

            for bond, reason in recommended_bonds:
                st.write(f"Bond: {bond}")
                st.write(f"Reason: {reason}")
                bond_stats = get_bond_statistics(bond)
                st.write("Bond Statistics:")
                for key, value in bond_stats.items():
                    st.write(f"{key}: {value}")
                st.write("---")


def request_feedback(request, result, model_id):
    """From a combination of request / result, displays a prefilled button to add feedback of the model specific model.

    Args:
        request (String): ISIN code
        result (List): Results given
        model_id (String): Identifier of the model for the feedback table
    """
    accept_button = st.button("Accept recommandation", key="accept_isin_feedback")
    deny_button = st.button("Deny recommandation", key="deny_isin_feedback")

    if accept_button:
        st.succes("Feedback added - Accepted recommandation !")
    elif deny_button:
        st.succes("Feedback added - Denied recommandation !")


# Run the page function
if __name__ == "__main__":
    main()
