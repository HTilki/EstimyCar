import streamlit as st
import polars as pl
from requete_dataframe import get_plage_annee, get_unique_moteur, get_unique_marque, get_unique_modele, get_unique_cylindre, get_unique_finition, get_unique_batterie, get_unique_generation
from machinelearning import predict_prix, predict_prix_autre_km
from numpy import ndarray

def display_km():
    km = st.sidebar.number_input("Kilométrage",  step=10000, min_value=0, max_value=1000000)
    return km

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

def select_annee(user_role, marque, modele) -> int:
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
    

def predict_button(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str):
    if st.button('Estimer la valeur du véhicule.'):
        data = transform_input(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
        st.write('Prix estimé : ', format_prediction(predict_prix(data, marque)))

def transform_input(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str) -> pl.DataFrame:
    data = pl.DataFrame(
        {
            'annee': annee, 
            'kilometrage': km,
            'boite': boite,
            'energie': energie,
            'marque': marque,
            'modele': modele,
            'generation': generation,
            'cylindre': cylindre,
            'moteur': moteur,
            'puissance': puissance,
            'finition': finition,
            'batterie': batterie
        }
    )
    return data

def format_prediction(prix_predit: ndarray) -> str:
    return str(prix_predit[0, 0]) + ' €' 


def predict_km_fictif_button(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str):
    if st.button('Estimer la valeur de votre véhicule selon le kilométrage.'):
        data = transform_input(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
        fig = predict_prix_autre_km(data, marque)
        st.plotly_chart(fig)
