import streamlit as st
import pandas as pd
import folium
from pages import page1, page2, page3, page4


APP_TITLE = "Natixis Business Challenge"
APP_SUB_TITLE = "Leverage flow business information to grow market making activity"

# Create a dictionary to map page names to page functions
pages = {
    "Page 1": page1.page1,
    "Page 2": page2.page2,
    "Page 3": page3.page3,
    "Page 4": page4.page4,
}

# Create a sidebar navigation menu
# st.sidebar.title("Navigation")
# selected_page = st.sidebar.selectbox("Go to", list(pages.keys()))

# Display the selected page
# pages[selected_page]()

st.set_page_config(APP_TITLE)
st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

st.subheader(
    "Welcome ! \nThe purpose of this Streamlit application is to provide a friendly UI to have recommendations on bonds and investors, actionnable insights on past trading data and information about the model used."
)
