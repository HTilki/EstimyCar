import streamlit as st
from streamlit_option_menu import option_menu
from webscraping import import_marques_modeles
from requete_dataframe import get_count_car, get_avg_price, calcul_delta
from fonctions_requete import show_dataframe
from fonctions_menu import display_km_selection, marques_mutliselect, modeles_multiselect, boite_multiselect, display_annee, energie_multiselect, display_prix_selection
import polars as pl 
import duckdb

nom_marques_modeles = pl.DataFrame(import_marques_modeles())


st.set_page_config( 
    page_title="CarScraping",
    page_icon="🚗",
    layout="wide")

st.title("🚗 CarScraping")
st.sidebar.title("Menu")


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


user_role = st.sidebar.selectbox("Select Option", ["Acheteur", "Vendeur"])


if user_role == "Acheteur":

    col1, col2 = st.columns(2)
    tab_data, tab2 = st.tabs(["🗃 Data", ":balloon: fni"])
    
    st.sidebar.header("Caractéristiques")
    
    # marques
    marques = marques_mutliselect(nom_marques_modeles)

    # modeles
    modeles = modeles_multiselect(nom_marques_modeles, marques)

    # annee
    annee_min, annee_max = display_annee()

    # kilometre
    km_min, km_max = display_km_selection()
    
    boite = boite_multiselect()

    #energie
    energie = energie_multiselect()

    #prix
    prix_min, prix_max = display_prix_selection()
 
    with tab_data:
        col1.metric(
            label="Nombre total de voitures", 
            value=get_count_car(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max),
            delta=calcul_delta(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max))
        col2.metric(
            "Prix moyen", 
            value=get_avg_price(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max))
            
        show_dataframe(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max)


    if st.sidebar.button("Reset"):
        st.session_state.reset = True  # Mark reset as True if button is pressed
        st.experimental_rerun()  # Rerun the script
    else:
        st.session_state.reset = False

with tab2:
    st.balloons()
