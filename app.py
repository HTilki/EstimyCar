import streamlit as st
from fonctions_app.app.import_mm import import_marques_modeles
from fonctions_app.requetes.requetes_kpi import get_count_car, get_avg_price, calcul_delta
from fonctions_app.app.fonctions_tab import show_dataframe, predict_button, get_prix_pred_displayed, get_prix_moy_displayed,predict_km_fictif_button
from fonctions_app.app.fonctions_menu import *
import polars as pl
from fonctions_app.requetes.requetes_stats import show_selected_chart
from fonctions_app.app.accueil import *

nom_marques_modeles = pl.DataFrame(import_marques_modeles())

st.set_page_config( 
    page_title="CarScraping",
    page_icon="🚗",
    layout="wide")
st.title("🚗 CarScraping")

st.sidebar.title("Menu")
style_markdown()

user_role = st.sidebar.selectbox("Votre profil", 
                                ["Acheteur", "Vendeur"], 
                                placeholder="Choisir un profil",
                                index=None)


if user_role == None:
    accueil()

if user_role == "Acheteur":
    nb_annonces, prix_moyen = st.columns(2)
    tab_data, tab_stats, tab2 = st.tabs(["🗃 Data", "📊 Statistiques Descriptives", "🎈 Créateurs"])
    
    st.sidebar.header("Caractéristiques")
    marques = marques_select(nom_marques_modeles, user_role)
    modeles = modeles_select(nom_marques_modeles, marques, user_role)
    annee_min, annee_max = display_annee(user_role)
    km_min, km_max = display_km(user_role)
    boite = boite_select(user_role)
    energie = energie_select(user_role)
    prix_min, prix_max = display_prix_selection()
    with tab_data:
        with nb_annonces:
            with st.container(border=True):
                st.metric(
                label="Nombre total de voitures", 
                value=get_count_car(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max),
                delta=calcul_delta(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max))
        with prix_moyen:
            with st.container(border=True):
                st.metric(
                    "Prix moyen", 
                value=str(get_avg_price(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max, user_role)) + '€')
        show_dataframe(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max)

    with tab_stats:
        show_selected_chart()

    with tab2:
        st.balloons()
        with st.expander("**Cette app géniale ? Le fruit d'une alchimie numérique orchestrée par…**"):
            st.write("- 👩‍💻 Aybuké BICAT : https://github.com/aybuke-b")
            st.write("- 👨‍💻 Hassan TILKI : https://github.com/HTilki")


if user_role == "Vendeur":

    tab_prediction = st.tabs(["🎯 Estimation"])
    #estimation, estimation_km = st.columns(2)
    st.sidebar.header("Caractéristiques")
    
    marque = marques_select(nom_marques_modeles, user_role)
    modele = modeles_select(nom_marques_modeles, marque, user_role)
    annee = select_annee(user_role, marque, modele)
    moteur = moteur_select(marque, modele)
    cylindre = cylindre_select(marque, modele)
    puissance = display_puissance()
    km = display_km(user_role)
    boite = boite_select(user_role)
    energie = energie_select(user_role)
    batterie = batterie_select(energie)
    generation = generation_select(marque, modele)
    finition = finition_select(marque, modele)
    
    with st.container():
        predict_button(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition, user_role)
        resultat = st.empty()
        get_prix_pred_displayed()
        get_prix_moy_displayed()
    predict_km_fictif_button(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
