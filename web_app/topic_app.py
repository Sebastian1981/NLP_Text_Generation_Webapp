import streamlit as st
import json
import pandas as pd


from utility import parse_date_from_html, parse_title_from_html, google_query, convert_df

keywords = ['Finanzielle Hilfe im Alter', 
            'Rentner in Not',
            'Armut Senioren',
            'Altersarmut Frauen',
            'Renten Pay-Gap',
            'Unterstützung Rentner']


def run_generate_topics_app():
    # select keywords
    keywords_selected = st.multiselect("Select keywords", keywords)
    
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

    ## save locally     
    #with open('keywords.json', 'w') as f:
    #    json.dump(keywords_selected, f)
    ## open keyword file
    #with open('keywords.json') as f:
    #    keywords_selected = json.load(f)
    #st.write(keywords_selected)