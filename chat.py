import streamlit as st
import openai
from streamlit_chat import message
import os
#import secrets_beta
import re
from decouple import config
import pandas as pd
from io import StringIO
from preprocess import preprocess

# Setting page title and header
st.set_page_config(page_title="Claim Detector", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Claim Detector - Finds all the claims in your text </h1>", unsafe_allow_html=True)

# Set org ID and API key

openai.api_key = '' #config("OPENAI_API_KEY")

# Map model names to OpenAI model IDs

model = "text-davinci-003"
model_name = "text-davinci-003"

prompt_prefix = """You work in the Journalism Company and in the Fact Checking Department. 
Your role is to read through a news outlet and highlit sentences that contains the claims that should be checked.
Here is a news line, flag this sentence as True if it's a fact check worthy claim and False if it is not: """

# generate a response
def generate_response(prompt):

    try:
        completion = openai.Completion.create(
            model=model,
            prompt=prompt_prefix + prompt,
            max_tokens=256,
            temperature=0 #st.session_state['messages']
        )
        
        response = completion.choices[0].text

    except Exception as e:
        response = 'Error'
    
    return response


uploaded_file = st.text_input("Choose a file", r"C:\Users\akinr\Downloads\NG_SA02_090722_cleaned.txt")
if uploaded_file is not None:

    # Can be used wherever a "file-like" object is accepted:
    dataframe = preprocess(uploaded_file)
    result = []
    for i in range(len(dataframe)):
        output = generate_response(dataframe["claim"].iloc[i])
        result.append(output)
    dataframe['True_or_False'] = result
    st.write(dataframe)
    dataframe.to_csv('Chat_GPT_Claims.csv')

