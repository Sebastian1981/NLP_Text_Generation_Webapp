import streamlit as st
import json
import pandas as pd
import re
import openai



from utility import parse_date_from_html, \
                    parse_title_from_html, \
                    google_query, \
                    convert_df, \
                    chatgpt_generate_topics, \
                    chatgpt_query

# get api key for chat gpt
try: # this is for local runtime
    with open('.\private.txt', 'r') as f:
        content = f.read()
        key = re.findall(r'\'.*?\'', content)[0].strip('\'')
        openai.api_key = key
    f.close()
except: # this is for streamlit cloud runtime
    # Access the password
    key = st.secrets["api_key"]
    openai.api_key = key

# cache the keyword list
keyword_list = st.cache(
    lambda: [])()


def run_generate_topics_app(): 

    # add keywords
    keyword_input = st.text_input('Enter keyword: ')
    if keyword_input:
        keyword_list.append(keyword_input)

    # select keywords
    keywords_selected = (st.multiselect("Select keywords", keyword_list))
    keywords_selected = list(set(keywords_selected)) # delete duplicates

    if st.button('Reset Keywords List'):
        keyword_list.clear()

    # Query google keyword by keyword
    st.subheader("Query Keyword-Topics using Google Search")
    num_results = st.slider('Number google hits per keyword?', 1, 10, 3)
    if st.button('Query Google'):
        df_titles_google = google_query(keywords = keywords_selected, num_results = num_results)
        st.write(df_titles_google)
        # download data
        st.download_button(
            label = "Download CSV",
            data = convert_df(df_titles_google),
            file_name='titles_google.csv',
            mime='text/csv')

    # Query ChatGPT to generate new Topics
    st.subheader("Query ChatGPT to generate new Topics")
    num_topics = st.slider('Select Number of Topics Generated by ChatGPT', 1, 20, 5)
    if st.button('Query ChatGPT'):
        # make ChatGPT instruction
        instruction = chatgpt_generate_topics(keywords=keywords_selected, num_topics=num_topics)
        st.write('Your instruction for ChatGPT: ', instruction)
        # pass instruction to ChatGPT and generate topics
        df_titles_chatgpt = chatgpt_query(instruction, num_tokens=100)
        st.write(df_titles_chatgpt)