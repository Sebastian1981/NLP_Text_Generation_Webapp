import streamlit as st
from path import Path
from topic_app import run_generate_topics_app

# download Germany language model
import spacy
import subprocess

if spacy.util.get_package_path("de_core_news_lg") is not None:
    print("de_core_news_lg is already installed")
else:
    print("de_core_news_lg is not installed")
    subprocess.call(["python", "-m", "spacy", "download", "de_core_news_lg"])





def main():
    st.title("Demo NLP App for SEO-Text Generation using ChatGPT")

    menu = ["About", "Generate Topics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "About":
        st.subheader("About this Project:")
        # depending on deployment i.e. local, docker or streamlit clout try different paths
        try:
            st.markdown(Path('about.md').read_text())
        except:
            st.markdown(Path('./web_app/about.md').read_text())   
    elif choice == "Generate Topics":
        st.subheader('Select Keywords')
        run_generate_topics_app()
    
if __name__ == "__main__":
    main()