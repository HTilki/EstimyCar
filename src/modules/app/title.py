import streamlit as st

def style_markdown():
    st.markdown(
        """
        <style>
                .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 2rem;
                    padding-right: 2rem;
                }
                .st-emotion-cache-16txtl3{
                    padding-top: 2rem;
                    padding-right: 0rem;
                    padding-bottom: 1rem;
                    padding-left: 0rem;
                }
        </style>
        """,
        unsafe_allow_html=True,
    )

def title():
    st.set_page_config( 
    page_title="EstimyCar",
    page_icon="🚗",
    layout="wide")
    st.title("🚗 Esti*my*:red[Car]")

    st.sidebar.title("Menu")
    style_markdown()