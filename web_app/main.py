import streamlit as st
from path import Path
from keyword_app import run_keyword_selection_app

def main():
    st.title("Demo NLP App for Text Generation using ChatGPT")

    menu = ["About", "Keywords"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "About":
        st.subheader("About this Project:")
        # depending on deployment i.e. local, docker or streamlit clout try different paths
        try:
            st.markdown(Path('About.md').read_text())
        except:
            st.markdown(Path('\web_app\About.md').read_text())   
    elif choice == "Keywords":
        st.subheader('Select Keywords')
        run_keyword_selection_app()
    
if __name__ == "__main__":
    main()