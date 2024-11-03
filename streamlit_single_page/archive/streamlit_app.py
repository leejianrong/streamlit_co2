import streamlit as st
import pandas as pd
import os
import altair as alt

# Load the data from CSV
@st.cache_data
def load_data(folder_path='./csv_data'):
    dataframes_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            key_for_df = os.path.splitext(filename)[0]
            dataframes_dict[key_for_df] = df
    return dataframes_dict

# Function to plot emissions data using Altair
def plot_emissions(data, title):
    # Ensure the 'Date' column is correctly parsed
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

    # Melt the DataFrame to long format for Altair
    data_melted = data.melt(id_vars='Date', var_name='Country/Sector', value_name='CO2 Emissions (Mt)')

    # Create an Altair line chart
    chart = alt.Chart(data_melted).mark_line(point=True).encode(
        x='Date:T',
        y='CO2 Emissions (Mt):Q',
        color='Country/Sector:N',
        tooltip=['Date:T', 'Country/Sector:N', 'CO2 Emissions (Mt):Q']
    ).properties(
        title=title
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# Streamlit UI
st.title("CO2 Emissions Data Visualization")
data_dict = load_data()
user_prompt = st.text_input("Enter a prompt for the data visualization:")

if user_prompt:
    if "annual emissions" in user_prompt.lower():
        st.subheader("Annual Emissions by Country")
        st.write(data_dict["annual_emissions_by_country"])
        countries = st.multiselect("Select countries to visualize:", 
                                    data_dict["annual_emissions_by_country"]["country_name"].unique())
        if countries:
            filtered_data = data_dict["annual_emissions_by_country"][
                data_dict["annual_emissions_by_country"]["country_name"].isin(countries)]
            plot_emissions(filtered_data, "Annual CO2 Emissions by Country")
    
    elif "daily emissions" in user_prompt.lower():
        st.subheader("Daily Emissions by Country")
        st.write(data_dict["daily_emissions_by_country"])
        countries = st.multiselect("Select countries to visualize:", 
                                    data_dict["daily_emissions_by_country"].columns[1:])
        if countries:
            filtered_data = data_dict["daily_emissions_by_country"][["Date"] + countries]
            plot_emissions(filtered_data, "Daily CO2 Emissions by Country")
    
    elif "aviation sector" in user_prompt.lower():
        st.subheader("Daily Emissions in Aviation Sector")
        st.write(data_dict["daily_emissions_by_country_aviation_sector"])
        plot_emissions(data_dict["daily_emissions_by_country_aviation_sector"], 
                       "Daily CO2 Emissions in Aviation Sector")
    
    elif "ground transportation" in user_prompt.lower():
        st.subheader("Daily Emissions in Ground Transportation Sector")
        st.write(data_dict["daily_emissions_by_country_ground_transportation_sector"])
        plot_emissions(data_dict["daily_emissions_by_country_ground_transportation_sector"], 
                       "Daily CO2 Emissions in Ground Transportation Sector")
    
    elif "industrial sector" in user_prompt.lower():
        st.subheader("Daily Emissions in Industrial Sector")
        st.write(data_dict["daily_emissions_by_country_industrial_sector"])
        plot_emissions(data_dict["daily_emissions_by_country_industrial_sector"], 
                       "Daily CO2 Emissions in Industrial Sector")
    
    elif "power sector" in user_prompt.lower():
        st.subheader("Daily Emissions in Power Sector")
        st.write(data_dict["daily_emissions_by_country_power_sector"])
        plot_emissions(data_dict["daily_emissions_by_country_power_sector"], 
                       "Daily CO2 Emissions in Power Sector")
    
    elif "residential sector" in user_prompt.lower():
        st.subheader("Daily Emissions in Residential Sector")
        st.write(data_dict["daily_emissions_by_country_residential_sector"])
        plot_emissions(data_dict["daily_emissions_by_country_residential_sector"], 
                       "Daily CO2 Emissions in Residential Sector")
    
    elif "global daily mean" in user_prompt.lower():
        st.subheader("Global Daily Mean Emissions")
        st.write(data_dict["global_daily_mean_emissions"])
        plot_emissions(data_dict["global_daily_mean_emissions"], "Global Daily Mean CO2 Emissions")
    
    elif "global emissions by sector" in user_prompt.lower():
        st.subheader("Global Emissions by Sector")
        st.write(data_dict["global_emissions_by_sector"])
        plot_emissions(data_dict["global_emissions_by_sector"], "Global CO2 Emissions by Sector")
    
    else:
        st.write("Sorry, I could not understand your prompt.")
