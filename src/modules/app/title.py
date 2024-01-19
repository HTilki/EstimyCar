import streamlit as st

def style_markdown():
    """
    Applique un style personnalisé avec des règles de style CSS pour ajuster le padding de certains éléments dans l'interface Streamlit.

    """
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
    """
    Configure le titre de la page et affiche le titre principal et le menu dans l'interface Streamlit.
    """
    st.set_page_config( 
    page_title="EstimyCar",
    page_icon="🚗",
    layout="wide")
    st.title("🚗 Esti*my*:red[Car]")

    st.sidebar.title("Menu")
    style_markdown()