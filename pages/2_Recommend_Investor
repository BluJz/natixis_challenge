import streamlit as st
import pandas as pd
import altair as alt
from utils.data_extraction import load_meteo_data

def plot_daily():
    st.subheader('Données aggrégées par jour')
    df_meteo = load_meteo_data()

    # Reset index to make 'date' a column
    df_meteo_reset = df_meteo.reset_index()

    # Group by 'date' and calculate the mean for each date
    mean_per_date = df_meteo_reset.groupby('date').mean()
    mean_per_date.drop(columns=['latitude', 'longitude'], inplace=True)
    mean_per_date = mean_per_date.reset_index()

    # User input for the year
    year = st.number_input("Sélectionnez l'année", min_value=2000, max_value=2021, value=2020)

    # Selector for the meteorological data column
    meteo_column = st.selectbox("Sélectionnez la variable météorologique à afficher", 
                                mean_per_date.columns.drop('date'))

    # Filter the data from September of the selected year to August of the next year
    start_date = pd.to_datetime(f"{year-1}-09-01")
    end_date = pd.to_datetime(f"{year}-08-31")
    filtered_df = mean_per_date[(mean_per_date['date'] >= start_date) & (mean_per_date['date'] <= end_date)]
    mean_per_date = filtered_df.groupby('date').mean().reset_index()
    mean_per_date['day_of_year'] = mean_per_date['date'].dt.dayofyear

    # Calculate the overall daily mean across all years
    df_meteo_reset['day_of_year'] = df_meteo_reset['date'].dt.dayofyear
    overall_mean = df_meteo_reset.groupby('day_of_year').mean().reset_index()
    overall_mean = overall_mean.merge(mean_per_date[['day_of_year', 'date']], how='left', on='day_of_year')

    # Base line chart for selected year
    line_chart = alt.Chart(mean_per_date).mark_line().encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f'{meteo_column}:Q', title=meteo_column.capitalize()),
    )

    # Line chart for overall mean
    mean_line_chart = alt.Chart(overall_mean).mark_line(color='red').encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f'{meteo_column}:Q', title='Mean ' + meteo_column.capitalize()),
    )

    # Transparent selector across the chart
    selectors = alt.Chart(mean_per_date).mark_rule().encode(
        x='date:T',
        opacity=alt.value(0),
        tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip(f'{meteo_column}:Q', title=meteo_column.capitalize())]
    ).add_selection(
        alt.selection_single(fields=['date'], nearest=True, on='mouseover', empty='none')
    )

    # Combine the charts
    chart = alt.layer(line_chart, mean_line_chart, selectors).properties(
        width=700,
        height=400
    ).interactive()

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

def plot_monthly():
    st.subheader('Données aggrégées par mois')
    df_meteo = load_meteo_data()

    # Reset index to make 'date' a column
    df_meteo_reset = df_meteo.reset_index()

    # Group by 'date' and calculate the mean for each date
    mean_per_date = df_meteo_reset.groupby('date').mean()
    mean_per_date.drop(columns=['latitude', 'longitude'], inplace=True)
    mean_per_date = mean_per_date.reset_index()

    # User input for the year
    year = st.number_input("Sélectionnez l'année", min_value=2000, max_value=2021, value=2020)

    # Selector for the meteorological data column
    meteo_column = st.selectbox("Sélectionnez la variable météorologique à afficher", 
                                mean_per_date.columns.drop('date'))

    # Filter the data from September of the selected year to August of the next year
    start_date = pd.to_datetime(f"{year-1}-09-01")
    end_date = pd.to_datetime(f"{year}-08-31")
    filtered_df = mean_per_date[(mean_per_date['date'] >= start_date) & (mean_per_date['date'] <= end_date)]
    # Group by year and month and calculate the mean
    monthly_means = filtered_df.groupby([filtered_df['date'].dt.year.rename('year'), filtered_df['date'].dt.month.rename('month')]).mean()
    # Reset the index to turn the grouping columns back into regular columns
    monthly_means = monthly_means.reset_index()
    # Create a new 'date' column with the first day of each month
    monthly_means['date'] = pd.to_datetime(monthly_means.rename(columns={'date': 'year'}).apply(lambda row: f"{int(row['year'])}-{int(row['month'])}-01", axis=1))

    # Calculate the overall daily mean across all years
    df_meteo_reset['month'] = df_meteo_reset['date'].dt.month
    overall_mean = df_meteo_reset.groupby('month').mean().reset_index()
    overall_mean = overall_mean.merge(monthly_means[['month', 'date']], how='left', on='month')

    # Base line chart for selected year
    line_chart = alt.Chart(monthly_means).mark_line().encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f'{meteo_column}:Q', title=meteo_column.capitalize()),
    )

    # Line chart for overall mean
    mean_line_chart = alt.Chart(overall_mean).mark_line(color='red').encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f'{meteo_column}:Q', title='Mean ' + meteo_column.capitalize()),
    )

    # Transparent selector across the chart
    selectors = alt.Chart(monthly_means).mark_rule().encode(
        x='date:T',
        opacity=alt.value(0),
        tooltip=[alt.Tooltip('date:T', title='Date'), alt.Tooltip(f'{meteo_column}:Q', title=meteo_column.capitalize())]
    ).add_selection(
        alt.selection_single(fields=['date'], nearest=True, on='mouseover', empty='none')
    )

    # Combine the charts
    chart = alt.layer(line_chart, mean_line_chart, selectors).properties(
        width=700,
        height=400
    ).interactive()

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


if __name__ == '__main__':
    st.title('Dashboard variables météorologiques')

    # Add a radio button to select the function
    date_range_selection = st.radio("Choisissez l'échelle de temps:", ('Par mois', 'Par jour'))

    # Call the appropriate function based on the selection
    if date_range_selection == 'Par mois':
        plot_monthly()
    elif date_range_selection == 'Par jour':
        plot_daily()