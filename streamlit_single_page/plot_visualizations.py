
import streamlit as st
import pandas as pd

def plot_visualizations(data_dict):
    st.title("CO2 Emissions by Sector in Japan and China")

    # Load the relevant data
    emissions_df = data_dict["global_emissions_by_sector"]

    # Convert the 'Date' column to datetime format
    emissions_df['Date'] = pd.to_datetime(emissions_df['Date'], dayfirst=True)

    # Sidebar for selecting the country to display
    countries = ["Japan", "China"]
    selected_country = st.sidebar.selectbox("Select Country", countries)

    if selected_country == "Japan":
        emissions_df_country = data_dict["daily_emissions_by_country_power_sector"]
        emissions_df_country = emissions_df_country[['Date', 'Japan']]
    elif selected_country == "China":
        emissions_df_country = data_dict["daily_emissions_by_country_power_sector"]
        emissions_df_country = emissions_df_country[['Date', 'China']]
    
    # Filter data by selected country
    emissions_df_country['Date'] = pd.to_datetime(emissions_df_country['Date'], dayfirst=True)

    # Plot the emissions by sector globally
    st.write("### Global Emissions by Sector")
    sectors = emissions_df.columns.drop('Date')
    st.line_chart(emissions_df.set_index('Date')[sectors])

    # Plot the emissions for the selected country
    st.write(f"### Emissions in {selected_country}")
    st.line_chart(emissions_df_country.set_index('Date')) 

