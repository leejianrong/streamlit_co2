import streamlit as st
import altair as alt
import pandas as pd
import os

st.set_page_config(
    page_title="CO2 Visualization App",
    page_icon="💨",
)

st.write("# CO2 Emissions Visualization")


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
annual_df = data_dict["annual_emissions_by_country"]
global_df = data_dict["daily_emissions_by_country"]

# Sidebar for search
st.sidebar.header("Visualization Prompt")
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""

def submit():
    st.session_state.prompt_text = st.session_state.widget
    st.session_state.widget = ""

st.sidebar.text_input("Enter visualization prompt", key="widget", on_change=submit)

prompt_text = st.session_state.prompt_text

st.write(prompt_text)

# Filter options
st.header("Filter Options")

# Select countries for visualization
countries = st.multiselect(
    "Select Country/Countries",
    options=annual_df["country_name"].unique(),
    default=["United States", "China"]  # Default selection
)

# Select year range
year_range = st.slider(
    "Select Year Range",
    int(annual_df["year"].min()),
    int(annual_df["year"].max()),
    (int(annual_df["year"].min()), int(annual_df["year"].max()))
)

# Filter data based on selections
filtered_data = annual_df[(annual_df["country_name"].isin(countries)) & 
                        (annual_df["year"].between(year_range[0], year_range[1]))]

# Display filtered data (optional)

if st.checkbox('Show filtered data'):
    st.subheader('Filtered data')
    st.write(filtered_data)

# Pivot data for plotting
plot_data = filtered_data.pivot(index="year", columns="country_name", values="value")

# Plotting section
st.subheader("CO₂ Emissions Over Time")

# Streamlit line chart
if not plot_data.empty:
    st.line_chart(plot_data)
else:
    st.write("Please select a country and year range with data.")


# Bar Chart - Top 10 Countries by Latest CO2 Emissions
st.subheader("Countries by Latest CO2 Emissions (Bar Chart)")
# latest_country_emissions = annual_df[annual_df['year'] == annual_df['year'].max()]
# latest_country_emissions = latest_country_emissions[latest_country_emissions['value'] > 0]  # Filter out zero emissions
# top_countries = latest_country_emissions.nlargest(10, 'value')

top_country_bar_chart = alt.Chart(filtered_data).mark_bar(color="steelblue").encode(
    x=alt.X('country_name:N', title='Country', sort='-y'),
    y=alt.Y('value:Q', title='CO2 Emissions (Mt CO2)'),
    tooltip=['country_name', 'value']
).properties(
    width=700, height=400
)

st.altair_chart(top_country_bar_chart)


# Filter data for recent global emissions (for pie chart)
recent_global_df = global_df.iloc[-1].drop(["Date", "World"])  # Exclude "World" from pie chart data

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
