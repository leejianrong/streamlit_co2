import streamlit as st
import pandas as pd
import altair as alt
import os 

# Load data from the data_dict
@st.cache_data
def load_data(folder_path='.\csv_data'):
    dataframes_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            key_for_df = os.path.splitext(filename)[0]
            dataframes_dict[key_for_df] = df 
    return dataframes_dict

# Load data
data_dict = load_data()

# Load data from the data_dict
power_sector_df = data_dict["daily_emissions_by_country_power_sector"]
residential_sector_df = data_dict["daily_emissions_by_country_residential_sector"]

# Convert the 'Date' column to datetime
power_sector_df['Date'] = pd.to_datetime(power_sector_df['Date'], dayfirst=True)
residential_sector_df['Date'] = pd.to_datetime(residential_sector_df['Date'], dayfirst=True)

# Merge the two DataFrames on 'Date'
combined_df = pd.merge(power_sector_df, residential_sector_df, on='Date', suffixes=('_Power', '_Residential'))

# Streamlit app
st.title("Emissions: Power Sector vs Residential Sector")

# Line chart for power vs residential sector emissions
st.subheader("Line Chart: Power Sector vs Residential Sector")
line_chart = alt.Chart(combined_df).transform_fold(
    ['World_Power', 'World_Residential'],
    as_=['Sector', 'Emissions']
).mark_line().encode(
    x='Date:T',
    y='Emissions:Q',
    color='Sector:N'
).properties(
    width=700,
    height=400
)
st.altair_chart(line_chart)

# Area chart for power vs residential sector emissions
st.subheader("Area Chart: Power Sector vs Residential Sector")
area_chart = alt.Chart(combined_df).transform_fold(
    ['World_Power', 'World_Residential'],
    as_=['Sector', 'Emissions']
).mark_area(opacity=0.3).encode(
    x='Date:T',
    y='Emissions:Q',
    color='Sector:N'
).properties(
    width=700,
    height=400
)
st.altair_chart(area_chart)

# Stacked bar chart for a specific date
st.subheader("Stacked Bar Chart for Specific Date")
selected_date = st.date_input('Select a date for the stacked bar chart', value=pd.to_datetime('2020-01-01'))
bar_chart_data = combined_df[combined_df['Date'] == pd.to_datetime(selected_date)]
stacked_bar_chart = alt.Chart(bar_chart_data.melt('Date', value_vars=['World_Power', 'World_Residential'], var_name='Sector', value_name='Emissions')).mark_bar().encode(
    x='Sector:N',
    y='Emissions:Q',
    color='Sector:N'
).properties(
    width=700,
    height=400
)
st.altair_chart(stacked_bar_chart)