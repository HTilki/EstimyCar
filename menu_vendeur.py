import streamlit as st
import polars as pl
from requetes_dataframe import *
from requetes_val_unique import *

def display_km(user_role):
    if user_role == "Vendeur":
        km = st.sidebar.number_input("Kilométrage",  step=10000, min_value=0, max_value=1000000)
        return km
    elif user_role == "Acheteur":
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

def display_puissance():
    ch = st.sidebar.number_input("Puissance",  step=10, min_value=0, max_value=1500)
    return ch

def marque_select() -> str:
    marques = get_unique_marque()
    choix_marque = st.sidebar.selectbox("Marque", marques,
                                        placeholder="Choisir une marque")
    return choix_marque
    
def modele_select(choix_marque: str) -> str:
    modeles = get_unique_modele(choix_marque)
    choix_modele = st.sidebar.selectbox("Modèle", modeles,
                                        placeholder="Choisir un modèle")
    return choix_modele

def generation_select(choix_marque: str, choix_modele: str) -> str:
    generations = get_unique_generation(choix_marque, choix_modele) + ["Autre choix..."]
    choix_generation = st.sidebar.selectbox("Génération", generations,
                                        index=None,
                                        placeholder="Choisir la génération")
    if choix_generation == "Autre choix...": 
        choix_generation_2 = st.sidebar.text_input("Autre choix de génération",
                                               placeholder="Saisissez la génération")
        return choix_generation_2
    elif choix_generation == None: 
        return 'null'
    else:
        return choix_generation


def moteur_select(choix_marque: str, choix_modele: str) -> str:
    moteurs = get_unique_moteur(choix_marque, choix_modele) + ["Autre choix..."]
    choix_moteur = st.sidebar.selectbox("Moteur", moteurs,
                                        index=None,
                                        placeholder="Choisir un moteur")
    if choix_moteur == "Autre choix...": 
        choix_moteur_2 = st.sidebar.text_input("Autre choix de moteur",
                                               placeholder="Saisissez votre moteur")
        return choix_moteur_2
    elif choix_moteur == None: 
        return 'null'
    else : 
        return choix_moteur


def cylindre_select(choix_marque: str, choix_modele: str) -> str:
    cylindres = get_unique_cylindre(choix_marque, choix_modele) + ["Autre choix..."]
    choix_cylindre = st.sidebar.selectbox("Cylindre", cylindres,
                                        index=None,
                                        placeholder="Choisir un cylindre")
    if choix_cylindre == "Autre choix...": 
        choix_cylindre_2 = st.sidebar.text_input("Autre choix de cylindre",
                                               placeholder="Exemple: 4.0")
        return choix_cylindre_2
    elif choix_cylindre == None: 
        return 'null'
    else : 
        return choix_cylindre
    
def finition_select(choix_marque: str, choix_modele: str) -> str:
    finitions = get_unique_finition(choix_marque, choix_modele) + ["Autre choix..."]
    choix_finition = st.sidebar.selectbox("Finition", finitions,
                                        index=None,
                                        placeholder="Choisir une finition")
    if choix_finition == "Autre choix...": 
        choix_finition_2 = st.sidebar.text_input("Autre choix de finition",
                                               placeholder="Choisir une finition")
        return choix_finition_2
    elif choix_finition == None: 
        return 'null'
    else : 
        return choix_finition


def boite_select() -> str:
    type_boite = ["Automatique", "Manuelle"]
    boite = st.sidebar.selectbox("Boite", type_boite,
                                 index=None,
                                 placeholder="Choisir un type de boite"
                                )
    if boite != None:
        return boite
    else:
        return 'null'

def select_annee(user_role: str, marque: str = "", modele: str = "") -> int:
    annee_min, annee_max = get_plage_annee(user_role, marque, modele)
    annee = range(annee_min, annee_max + 1, 1)
    annee_choisi = st.sidebar.select_slider(
        "Année",
        options=sorted(annee),
        value=max(annee)
        )
    return annee_choisi

def energie_select() -> str:
    type_energie = [
        "Essence", 
        "Diesel",
        "Hybrides", 
        "Électrique", 
        "Bicarburation essence bioéthanol", 
        "Bicarburation essence / gpl"]
    energie = st.sidebar.selectbox("Énergie", type_energie,
                                    placeholder="Choisir un type d'énergie")
    if energie != None:
        return energie
    else:
        return 'null'

def batterie_select(energie: str) -> str:
    if energie == "Électrique":
        batteries = get_unique_batterie() + ["Autre choix..."]
        choix_batterie = st.sidebar.selectbox("Batterie", batteries,
                                            index=None,
                                            placeholder="Choisir une autonomie")
        if choix_batterie == "Autre choix...": 
            choix_batterie_2 = st.sidebar.text_input("Autre choix de batterie",
                                                placeholder="Exemple: 100kWh")
            return choix_batterie_2
        else: 
            return choix_batterie
    else: 
        return 'null'
    
