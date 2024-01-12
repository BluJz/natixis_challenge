import streamlit as st

# Placeholder functions for backend logic
def get_company_statistics(company_short_name):
    # Replace with actual logic to fetch company statistics
    return {"Revenue": "100M", "Employees": "500"}

def get_client_recommendations(bond_name):
    # Replace with actual logic to get client recommendations
    return [("Bond A", "High yield"), ("Bond B", "Stable investment"), ("Bond C", "Low risk")]

def get_bond_statistics(bond_name):
    # Replace with actual logic to fetch bond statistics
    return {"Yield": "5%", "Rating": "AAA"}

def page1():
    st.title("Client Recommender")
    st.write("Enter the ISIN of a bound and get the most recommended clients for this bound")

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
        if run_button and ISIN:
            st.write("Recommended Clients for:", ISIN)
            recommended_clients = get_clients_recommendations(ISIN)

            for bond, reason in recommended_clients:
                st.write(f"Client: {client}")
                st.write(f"Reason: {reason}")
                client_stats = get_client_statistics(client)
                st.write("Client Statistics:")
                for key, value in client_stats.items():
                    st.write(f"{key}: {value}")
                st.write("---")

# Run the page function
page1()