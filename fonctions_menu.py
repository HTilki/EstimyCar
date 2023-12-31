import streamlit as st
import polars as pl
from requete_dataframe import get_plage_annee

user_role = st.sidebar.selectbox("Select Option", ["Acheteur", "Vendeur"])

def display_km_selection():
    """
    Affiche des champs de saisie pour sélectionner un kilométrage minimal et maximal.

    """
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
    """
    Retourne une liste de marques de véhicules uniques pour utilisation dans un menu déroulant.

    ## Parameters:
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules.

    ## Returns:
        list: Liste triée de noms de marques uniques pour une utilisation dans un menu déroulant multi-sélection.
    """
    brands = nom_marques_modeles['marque'].unique().to_list()
    brands.sort()

    if user_role == "Acheteur":
        choix_marque = st.sidebar.multiselect("Marque", brands,
                                        placeholder="Choisir une/des marque(s)")
    else:
        choix_marque = st.sidebar.selectbox("Marque", brands,
                                        placeholder="Choisir une marque")
    return choix_marque
    
def modeles_multiselect(nom_marques_modeles: pl.DataFrame, choix_marque: list) -> list:
    """
    Retourne une liste triée de modèles de véhicules uniques, associés à une ou plusieurs marques sélectionnées,
    pour utilisation dans un menu déroulant. 

    ## Parameters:
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules.
        choix_marque (list): _description_

    ## Returns:
        list: Liste triée de noms de modèles uniques pour une utilisation dans un menu déroulant multi-sélection.
    """
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
    """
    Retourne une liste de types de boîtes de vitesse pour utilisation dans un menu déroulant.

    Returns:
        list: Liste des types de boîtes de vitesse sélectionnés. Si aucun choix n'est fait, retourne tous les
        types de boîtes disponibles.
    """
    type_boite = ["Automatique", "Manuelle"]
    boite = st.sidebar.multiselect("Boîte", type_boite,
                                placeholder="Choisir un type de boîte"
                                )
    if boite == []:
        boite = type_boite
    return boite

def display_annee():
    """
    Affiche une barre de sélection pour choisir une plage d'année.

    Returns:
        _type_: 
    """
    annee_min, annee_max = get_plage_annee()
    annee = range(annee_min, annee_max + 1, 1)
    annee_min, annee_max = st.sidebar.select_slider(
        "Année",
        options=sorted(annee),
        value=(min(annee), max(annee))
        )
    return annee_min, annee_max

def energie_multiselect() -> list:
    """
    Retourne une liste de types d'énergie pour utilisation dans un menu déroulant.

    Returns:
        list: Liste des types d'énergie sélectionnés. Si aucun choix n'est fait, retourne tous les
        types d'énergie disponibles.
    """
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
    """
    Affiche des champs de saisie pour sélectionner un prix minimal et maximal.
    """

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