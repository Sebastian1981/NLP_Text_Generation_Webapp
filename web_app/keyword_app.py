import streamlit as st

keywords = ['Finanzielle Hilfe im Alter', 
            'Rentner in Not',
            'Armut Senioren',
            'Altersarmut Frauen',
            'Renten Pay-Gap',
            'Unterstützung Rentner']


def run_keyword_selection_app():
    st.title("Keywords")
    keywords_selected = st.multiselect("Select keywords", keywords)
    
