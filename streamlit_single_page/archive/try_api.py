from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_TOKEN"])

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {
            "role": "user",
            "content": "write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)