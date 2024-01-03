import streamlit as st
from webscraping import import_marques_modeles
from requetes_kpi import get_count_car, get_avg_price, calcul_delta
from fonctions_tab import show_dataframe, predict_button, predict_km_fictif_button
from menu_acheteur import *
from menu_vendeur import *
import polars as pl

nom_marques_modeles = pl.DataFrame(import_marques_modeles())


st.set_page_config( 
    page_title="CarScraping",
    page_icon="🚗",
    layout="wide")
st.title("🚗 CarScraping")

st.sidebar.title("Menu")
style_markdown()

user_role = st.sidebar.selectbox("Selectionnez votre profil", ["Acheteur", "Vendeur"])


if user_role == "Acheteur":
    nb_annonces, prix_moyen = st.columns(2)
    tab_data, tab2 = st.tabs(["🗃 Data", ":balloon: fni"])
    
    st.sidebar.header("Caractéristiques")
    marques = marques_mutliselect(nom_marques_modeles)
    modeles = modeles_multiselect(nom_marques_modeles, marques)
    annee_min, annee_max = display_annee(user_role)
    km_min, km_max = display_km(user_role)
    boite = boite_multiselect()
    energie = energie_multiselect()
    prix_min, prix_max = display_prix_selection()
    with tab_data:
        nb_annonces.metric(
            label="Nombre total de voitures", 
            value=get_count_car(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max),
            delta=calcul_delta(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max))
        prix_moyen.metric(
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


if user_role == "Vendeur":

    tab_prediction = st.tabs(["Estimation"])
    estimation, estimation_km = st.columns(2)
    st.sidebar.header("Caractéristiques")
    
    marque = marque_select()
    modele = modele_select(marque)
    annee = select_annee(user_role, marque, modele)
    moteur = moteur_select(marque, modele)
    cylindre = cylindre_select(marque, modele)
    puissance = display_puissance()
    km = display_km(user_role)
    boite = boite_select()
    energie = energie_select()
    batterie = batterie_select(energie)
    # changer class de batterie en int ???
    generation = generation_select(marque, modele)
    finition = finition_select(marque, modele)
    with estimation:
        predict_button(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)

    with estimation_km:
        predict_km_fictif_button(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)

