import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static
from shapely.ops import nearest_points
import folium
from folium.features import GeoJsonTooltip
from utils.maps import create_map
from utils.data_extraction import load_communes_geometry, load_meteo_data_date


APP_TITLE = "Agricultural Yields in Eure and Eure-et-Loire Report"
APP_SUB_TITLE = "AXA Climate Process Project"

if __name__ == "__main__":
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    st.subheader('Welcome to the Streamlit app of this project, feel free to dive in each page of the app: the first one explores agricultural yields in the past 20 years, the second explores meteorological data and the third one explore each year one by one!')