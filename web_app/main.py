import streamlit as st
from path import Path
from topic_app import run_generate_topics_app

def main():
    st.title("Demo NLP App for Text Generation using ChatGPT")

    menu = ["About", "Generate Topics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "About":
        st.subheader("About this Project:")
        # depending on deployment i.e. local, docker or streamlit clout try different paths
        try:
            st.markdown(Path('About.md').read_text())
        except:
            st.markdown(Path('.\web_app\About.md').read_text())   
    elif choice == "Generate Topics":
        st.subheader('Select Keywords')
        run_generate_topics_app()
    
if __name__ == "__main__":
    main()