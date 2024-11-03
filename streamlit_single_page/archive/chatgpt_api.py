from openai import OpenAI
import streamlit as st
import importlib
import pandas as pd
import os
import re


PROMPT_ENGINEERING_MESSAGE = """
You are a Python programmer that creates visualization pages using Streamlit. After the user enters a prompt, write code for a plotting function. From the main file, the plotting function will be called to display graphs in the Streamlit app.

To handle date parsing issues, we can use the dayfirst=True parameter in pd.to_datetime() to accommodate date formats where the day comes before the month (like DD/MM/YYYY).

The CO2 emissions data is stored in multiple pandas DataFrames inside a dictionary. Here are the key strings that can be used access these DataFrames (column names in parentheses):

annual_emissions_by_country (country_code, country_name, year, value)
daily_emissions_by_country (Date, China, India, US, EU, Russia, Japan, Brazil, ROW, World) 
daily_emissions_by_country_aviation_sector (Date, China, India, US, EU, Russia, Japan, Brazil, ROW, Domestic Aviation, International Aviation, All Aviation) 
daily_emissions_by_country_ground_transportation_sector (Date, China, India, US, EU, Russia, Japan, Brazil, ROW, World) 
daily_emissions_by_country_industrial_sector (Date, China, India, US, EU, Russia, Japan, Brazil, ROW, World) 
daily_emissions_by_country_power_sector (Date, China, India, US, EU, Russia, Japan, Brazil, ROW, World) 
daily_emissions_by_country_residential_sector (Date, China, India, US, EU, Russia, Japan, Brazil, ROW, World) 
global_daily_mean_emissions (Mt CO2 per day, daily mean CO2) 
global_emissions_by_sector (Date, Power, Ground Transport, Industry, Residential, Aviation, International Shipping, Globe)

When writing the plotting function, use Streamlit to visualize what the user asks for. Answer only with the Python code. The data is stored in a variable called data_dict. Example usage:

data_dict["annual_emissions_by_country"]

After each users visualization prompt, provide code to implement this function:

def plot_visualizations(data_dict):
    # write your code here

Acknowledge these instructions with "I understand". From now on, I will act as the user, sending you prompts that I want you to help visualize in Streamlit.
"""
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

st.title("ChatGPT-like clone")
client = OpenAI(api_key=st.secrets["OPENAI_TOKEN"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.session_state.messages.append({"role": "system", "content": PROMPT_ENGINEERING_MESSAGE})
with st.chat_message("system"):
    st.markdown(PROMPT_ENGINEERING_MESSAGE)

with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

if prompt := st.chat_input("Enter visualization prompt"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    pattern = r"```python(.*?)```" 
    extracted_code = re.findall(pattern, response, re.DOTALL)[0]
    print(extracted_code)
    with open("plot_visualizations.py", "w") as f:  # overwrite the whole file
            f.write(extracted_code)
    import plot_visualizations  # Ensure the module is imported initially
    importlib.reload(plot_visualizations)  # Reload the module
    from plot_visualizations import plot_visualizations
    plot_visualizations(data_dict)
