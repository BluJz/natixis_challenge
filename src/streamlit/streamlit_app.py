import streamlit as st
import pandas as pd
import folium
from pages import page1, page2, page3, page4

APP_TITLE = "Natixis Business Challenge"
APP_SUB_TITLE = "Leverage flow business information to grow market making activity"

st.set_page_config(APP_TITLE, page_icon="📊")


# Fonction pour injecter du CSS personnalisé
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Utiliser cette fonction pour définir la couleur des en-têtes
def set_header_color():
    st.markdown(
        """
        <style>
        h1, h2, h3, h4, h5, h6 {
            color: #5F259F; /* Couleur violet Pantone */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Appliquer la couleur des en-têtes
set_header_color()

# Add this line to include an image banner
st.image("banner.png", use_column_width=True)

st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)

st.subheader(
    "Welcome ! \nThe purpose of this Streamlit application is to provide a friendly UI to have recommendations on bonds and investors, actionnable insights on past trading data and information about the model used."
)

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
