import streamlit as st
import pandas as pd
import folium


APP_TITLE = "Natixis Business Challenge"
APP_SUB_TITLE = "Leverage flow business information to grow market making activity"

if __name__ == "__main__":
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    st.subheader(
        "Welcome ! \nThe purpose of this Streamlit application is to provide a friendly UI to have recommendations on bonds and investors, actionnable insights on past trading data and information about the model used."
    )
