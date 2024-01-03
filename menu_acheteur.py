import streamlit as st
import polars as pl
from requetes_val_unique import get_plage_annee


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


def display_km_selection():

    kmmin, kmmax = st.sidebar.columns([1, 1])
    with kmmin:
        km_min = st.number_input("Km min",  step=10000, min_value=0, max_value=1000000)
    with kmmax:
        km_max = st.number_input("Km max", step=10000, min_value=0, value=1000000, max_value=1000000)
    if km_min > km_max:
        st.warning("⚠️ La valeur min doit être inférieure à max !")
    st.markdown("""
    <style>
        button.step-up {display: none;}
        button.step-down {display: none;}
        div[data-baseweb] {border-radius: 4px;}
    </style>""",
    unsafe_allow_html=True)
    
    return km_min, km_max


def marques_mutliselect(nom_marques_modeles: pl.DataFrame) -> list:
    brands = nom_marques_modeles['marque'].unique().to_list()
    brands.sort()
    choix_marque = st.sidebar.multiselect("Marque", brands,
                                          placeholder="Choisir une/des marque(s)")
    return choix_marque
    
def modeles_multiselect(nom_marques_modeles: pl.DataFrame, choix_marque: list) -> list:
    if not choix_marque:  # Si aucune marque n'est sélectionnée
        modeles = [modele for modeles_list in nom_marques_modeles['modeles'] for modele in modeles_list]
        modeles = list(set(modeles))
        modeles.sort()
    else:
        modeles = []
        # Parcourir les lignes du DataFrame en utilisant la méthode zip
        for marque, modeles_list in zip(nom_marques_modeles['marque'], nom_marques_modeles['modeles']):
            if marque in choix_marque:
                modeles.extend(modeles_list)
        modeles = list(set(modeles))
        modeles.sort()

    choix_modele = st.sidebar.multiselect("Modèle", modeles,
                                          placeholder="Choisir un/des modèle(s)")
    return choix_modele

def boite_multiselect() -> list:
    type_boite = ["Automatique", "Manuelle"]
    boite = st.sidebar.multiselect("Boite", type_boite,
                                   placeholder="Choisir un type de boite"
                                   )
    if boite == []:
        boite = type_boite
    return boite

def display_annee(user_role):
    annee_min, annee_max = get_plage_annee(user_role)
    annee = range(annee_min, annee_max + 1, 1)
    annee_min, annee_max = st.sidebar.select_slider(
        "Année",
        options=sorted(annee),
        value=(min(annee), max(annee))
        )
    return annee_min, annee_max

def energie_multiselect() -> list:
    type_energie = [
        "Essence", 
        "Diesel",
        "Hybrides", 
        "Électrique", 
        "Bicarburation essence bioéthanol", 
        "Bicarburation essence / gpl"]
    energie = st.sidebar.multiselect("Énergie", type_energie,
                                    placeholder="Choisir un type d'énergie")
    
    if energie == []:
        energie = type_energie
    return energie

def display_prix_selection():

    prixmin, prixmax = st.sidebar.columns([1, 1])
    with prixmin:
        prix_min = st.number_input("Prix min",  step=1000, min_value=0, max_value=3000000)
    with prixmax:
        prix_max = st.number_input("Prix max", step=1000, min_value=0, value=3000000, max_value=3000000)
    if prix_min > prix_max:
        st.warning("⚠️ La valeur min doit être inférieure à max !")
    st.markdown("""
    <style>
        button.step-up {display: none;}
        button.step-down {display: none;}
        div[data-baseweb] {border-radius: 4px;}
    </style>""",
    unsafe_allow_html=True)
    
    return prix_min, prix_max