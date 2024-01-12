import streamlit as st

# Placeholder functions for backend logic
def get_company_statistics(company_short_name):
    # Replace with actual logic to fetch company statistics
    return {"Revenue": "100M", "Employees": "500"}

def get_bond_recommendations(company_short_name):
    # Replace with actual logic to get bond recommendations
    return [("Bond A", "High yield"), ("Bond B", "Stable investment"), ("Bond C", "Low risk")]

def get_bond_statistics(bond_name):
    # Replace with actual logic to fetch bond statistics
    return {"Yield": "5%", "Rating": "AAA"}

def page1():
    st.title("Company Bond Recommender")
    st.write("Enter the name of a company and get the most recommended bonds for this client")

    # Layout: Two columns
    col1, col2 = st.columns(2)

    # Column 1: Company Search and Statistics
    with col1:
        company_short_name = st.text_input("Enter Company Short Name")
        run_button = st.button("Run Recommender")
        
        if run_button and company_short_name:
            st.write("Company Statistics:")
            company_stats = get_company_statistics(company_short_name)
            for key, value in company_stats.items():
                st.write(f"{key}: {value}")

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

# Run the page function
page1()