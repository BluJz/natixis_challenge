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
    """, unsafe_allow_html=True,
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


def main():
    set_header_color()
    st.title("ISIN-Based Company Recommender")
    st.write("Enter an ISIN code and get recommended companies")

    isin_code = st.text_input("Enter ISIN Code")
    run_button = st.button("Run Recommender", key="isin_to_company_recommender")

    # Layout: Two columns
    col1, col2 = st.columns(2)

    # Column 1: ISIN Input and Statistics
    with col1:
        if run_button and isin_code:
            st.subheader("ISIN Code Statistics:")
            isin_stats = get_isin_statistics(isin_code)
            if isin_stats is not None:
                donnees = []
                for item in isin_stats:
                    donnees += [item]
                df = pd.DataFrame(donnees, columns=['Total Traded Volume', 'Mid Price($)', 'Rating'])
                st.table(df)
            else :
                st.write("Not available")

    # Column 2: Company Recommendations and Statistics
    with col2:
        if run_button and isin_code:
            st.subheader("Recommended Companies for ISIN:", isin_code)
            recommended_companies = get_company_recommendations(isin_code)

            for company, reason in recommended_companies:
                st.write(f"Company: {company}")
                st.write(f"Reason: {reason}")
                company_stats = get_company_statistics(company)
                st.write("Company Statistics:")
                for key, value in company_stats.items():
                    st.write(f"{key}: {value}")
                st.write("---")


# Run the page function
if __name__ == "__main__":
    main()
