import streamlit as st
import altair as alt
import pandas as pd
import os
from plot_visualizations import plot_visualizations
from openai import OpenAI
import sys
import re
import importlib
from utils import PROMPT_ENGINEERING_MESSAGE, DEFAULT_FUNCTION_CODE

hasFailedBefore = False

# Initialize OpenAI client with API key
client = OpenAI(api_key=st.secrets["OPENAI_TOKEN"])

# Set default model if not in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []


# Configure Streamlit app
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

# Sidebar for search
st.sidebar.header("Visualization Prompt")
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""

messages = [{"role": "system", "content": PROMPT_ENGINEERING_MESSAGE}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

print(completion.choices[0].message.content)

def submit(error_message = ""):

    # Update session state with input prompt
    
    if(not hasFailedBefore):
        st.session_state.prompt_text = st.session_state.widget
    else:
        st.session_state.prompt_text = "Last attempt failed try again, error message: " + error_message
    st.session_state.widget = ""

    # Call the LLM model
    if st.session_state.prompt_text:
        try:
            messages.append({"role":"user","content":st.session_state.prompt_text})
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            generated_text = completion.choices[0].message.content

            # write the response to file
            pattern = r"```python(.*?)```"
            matching_list = re.findall(pattern, generated_text, re.DOTALL)
            if matching_list:
                with open("plot_visualizations.py", "w") as f:  # overwrite the whole file
                    extracted_code = matching_list[0]
                    f.write(extracted_code)
            else:
                with open("plot_visualizations.py", "w") as f:  # overwrite the whole file
                    f.write(DEFAULT_FUNCTION_CODE)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            st.error(f"An error occurred: {exc_type}, {exc_tb.tb_lineno}")


import plot_visualizations
importlib.reload(plot_visualizations)
from plot_visualizations import plot_visualizations

# Display current prompt
st.write("### Current Prompt")
st.write(st.session_state.prompt_text)
try:
    plot_visualizations(data_dict)
except Exception as e:
    if(not hasFailedBefore):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error_msg = f"An error occurred: {exc_type}, {exc_tb.tb_lineno}"
        hasFailedBefore = True
        print("failed just once; calling submit again.")
        submit(error_message=error_msg)
    else:
        st.exception(e)
        
    
st.sidebar.text_input("Enter visualization prompt", key="widget", on_change=submit)


