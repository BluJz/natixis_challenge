import streamlit as st
from sql_querier import sql_querier
import pandas as pd


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


def main():
    set_header_color()
    st.title("Company Bond Recommender")
    st.write(
        "Enter the name of a company and get the most recommended bonds for this client"
    )

    # Layout: Two columns
    col1, col2 = st.columns(2)

    # Column 1: Company Search and Statistics
    with col1:
        company_short_name = st.text_input("Enter Company Short Name")
        run_button = st.button("Run Recommender", key="company_to_isin_recommender")

        if run_button and company_short_name:
            st.write("Company Statistics:")
            company_stats = get_company_statistics(company_short_name)
            if company_stats is not None:
                donnees = []
                for item in company_stats:
                    donnees += [item]
                df = pd.DataFrame(donnees, columns=["ISIN", "Rating", "Montant"])
                st.write("3 most recent client transactions:")
                st.table(df)
            else:
                st.write("Not available")

    # Column 2: Bond Recommendations and Statistics
    with col2:
        if run_button and company_short_name:
            st.write("Recommended Bonds for:", company_short_name)
            recommended_bonds = get_bond_recommendations(company_short_name)

            for bond, reason in recommended_bonds:
                st.write(f"Bond: {bond}")
                st.write(f"Reason: {reason}")
                bond_stats = get_bond_statistics(bond)
                st.write("Bond Statistics:")
                for key, value in bond_stats.items():
                    st.write(f"{key}: {value}")
                st.write("---")

def request_


# Run the page function
if __name__ == "__main__":
    main()
