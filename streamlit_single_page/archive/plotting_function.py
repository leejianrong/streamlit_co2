import streamlit as st
import pandas as pd
import altair as alt

def plotting_function(dataframes_dict):
    st.title("CO2 Emissions Data Insights by Country")

    # Load relevant data
    annual_df = dataframes_dict["annual_emissions_by_country"]
    global_df = dataframes_dict["daily_emissions_by_country"]

    # Select a country
    country = st.selectbox("Select Country", annual_df['country_name'].unique())
    
    # Filter data for the selected country
    country_annual_df = annual_df[annual_df['country_name'] == country]
    
    # Filter data for recent global emissions (for pie chart)
    recent_global_df = global_df.iloc[-1].drop(["Date", "World"])  # Exclude "World" from pie chart data

    # Layout with multiple columns for different plots
    st.header(f"CO2 Emission Analysis for {country}")

    col1, col2 = st.columns(2)

    # Bar Chart - Annual CO2 Emissions
    with col1:
        st.subheader("Annual CO2 Emissions (Bar Chart)")
        bar_chart = alt.Chart(country_annual_df).mark_bar(color="teal").encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('value:Q', title='CO2 Emissions (Mt CO2)'),
            tooltip=['year', 'value']
        ).properties(
            width=300, height=300
        )
        st.altair_chart(bar_chart)

    # Line Chart - Annual CO2 Emissions
    with col2:
        st.subheader("Annual CO2 Emissions (Line Chart)")
        line_chart = alt.Chart(country_annual_df).mark_line(point=True, color="orange").encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('value:Q', title='CO2 Emissions (Mt CO2)'),
            tooltip=['year', 'value']
        ).properties(
            width=300, height=300
        )
        st.altair_chart(line_chart)

    # Pie Chart - Latest Global Emissions Distribution (excluding "World")
    st.subheader("Latest Global CO2 Emissions Distribution (Pie Chart)")
    latest_emissions = recent_global_df.reset_index().rename(columns={recent_global_df.name: 'Emissions', 'index': 'Region'})
    pie_chart = alt.Chart(latest_emissions).mark_arc().encode(
        theta=alt.Theta(field="Emissions", type="quantitative"),
        color=alt.Color(field="Region", type="nominal"),
        tooltip=["Region", "Emissions"]
    ).properties(
        width=400, height=400
    )
    st.altair_chart(pie_chart)

    # Bar Chart - Top 10 Countries by Latest CO2 Emissions
    st.subheader("Top 10 Countries by Latest CO2 Emissions (Bar Chart)")
    latest_country_emissions = annual_df[annual_df['year'] == annual_df['year'].max()]
    latest_country_emissions = latest_country_emissions[latest_country_emissions['value'] > 0]  # Filter out zero emissions
    top_countries = latest_country_emissions.nlargest(10, 'value')

    top_country_bar_chart = alt.Chart(top_countries).mark_bar(color="steelblue").encode(
        x=alt.X('country_name:N', title='Country', sort='-y'),
        y=alt.Y('value:Q', title='CO2 Emissions (Mt CO2)'),
        tooltip=['country_name', 'value']
    ).properties(
        width=700, height=400
    )

    st.altair_chart(top_country_bar_chart)
