import streamlit as st
import polars as pl
from src.modules.requetes.requetes_dataframe import *
from src.modules.requetes.requetes_val_unique import *


def select_user_role() -> str:
    return st.sidebar.selectbox("Votre profil", 
                                ["Acheteur", "Vendeur"], 
                                placeholder="Choisir un profil",
                                index=None)


def display_km(user_role):
    """
    Affiche et gère l'entrée de kilométrage en fonction du rôle de l'utilisateur.

    ## Parameters:
        user_role (str) : le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        - Si l'utilisateur est un "Acheteur", affiche et gère la sélection 
                    du kilométrage minimum et maximum et renvoie ces valeurs sous forme de tuple.
        - Si l'utilisateur est un "Vendeur", renvoie le kilométrage saisi.
    """

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
            st.sidebar.warning("⚠️ La valeur min doit être inférieure à max !")
        st.markdown("""
        <style>
            button.step-up {display: none;}
            button.step-down {display: none;}
            div[data-baseweb] {border-radius: 4px;}
        </style>""",
        unsafe_allow_html=True)
        return km_min, km_max




def marques_select(nom_marques_modeles: pl.DataFrame, user_role) -> list:
    """
    Affiche une liste de marques de véhicules pour la sélection en fonction du rôle de l'utilisateur.

    ## Parameters:
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules. 
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    # #Returns:
        list: 
            - Si l'utilisateur est un "Acheteur", renvoie une liste d'une ou plusieurs marques sélectionnées.
            - Si l'utilisateur est un "Vendeur", renvoie la marque sélectionnée.
    """

    if user_role == "Acheteur":
        brands = nom_marques_modeles['marque'].unique().to_list()
        brands.sort()
        choix_marque = st.sidebar.multiselect("Marque", brands,
                                            placeholder="Choisir une/des marque(s)")
        return choix_marque
    elif user_role == "Vendeur":
        marques = get_unique_marque()
        choix_marque = st.sidebar.selectbox("Marque", marques,
                                        placeholder="Choisir une marque")
        return choix_marque
    


def modeles_select(nom_marques_modeles: pl.DataFrame, choix_marque: list, user_role) -> list:
    """
    Renvoie une sélection de modèles de véhicules en fonction de la marque sélectionnée et du rôle de l'utilisateur.

    ## Parameters:
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules. 
        choix_marque (list): Liste des marques sélectionnées au préalable.
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur").

    ## Returns:
        list: 
            - Si l'utilisateur est un "Acheteur", retourne une liste de modèles sélectionnés correspondant à/aux marque(s) choisie(s).
            - Si l'utilisateur est un "Vendeur", retourne le modèle sélectionné pour la marque spécifique.
    """

    if user_role == "Acheteur":
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
    
    elif user_role == "Vendeur":
        modeles = get_unique_modele(choix_marque)
        choix_modele = st.sidebar.selectbox("Modèle", modeles,
                                        placeholder="Choisir un modèle")
        return choix_modele




def boite_select(user_role) -> list:
    """
    Retourne une sélection de types de boîte en fonction du rôle de l'utilisateur.

    ## Parameters:
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        list: 
            - Si l'utilisateur est un "Acheteur", retourne une liste de types de boîte sélectionnés via une multisélection.
            - Si l'utilisateur est un "Vendeur", renvoie le type de boîte sélectionné via une liste déroulante. Si aucun choix n'est fait, renvoie "null".
    """

    if user_role == "Acheteur":
        type_boite = ["Automatique", "Manuelle"]
        boite = st.sidebar.multiselect("Boite", type_boite,
                                    placeholder="Choisir un type de boite")
        if boite == []:
            boite = type_boite
        return boite
    elif user_role == "Vendeur":
        type_boite = ["Automatique", "Manuelle"]
        boite = st.sidebar.selectbox("Boite", type_boite,
                                    index=None,
                                    placeholder="Choisir un type de boite"
                                    )
        if boite != None:
            return boite
        else:
            return 'null'
        


def energie_select(user_role) -> list:
    """
    Retourne une sélection de types d'énergie en fonction du rôle de l'utilisateur.

    ## Parameters:
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        list: 
            - Si l'utilisateur est un "Acheteur", retourne une liste de types d'énergie sélectionnés via une multisélection.
            - Si l'utilisateur est un "Vendeur", renvoie le type d'énergie sélectionné via une liste déroulante. Si aucun choix n'est fait, renvoie "null".
    """
    type_energie = [
        "Essence", 
        "Diesel",
        "Hybrides", 
        "Électrique", 
        "Bicarburation essence bioéthanol", 
        "Bicarburation essence / gpl"]
    if user_role == "Acheteur":
        energie = st.sidebar.multiselect("Énergie", type_energie,
                                    placeholder="Choisir un type d'énergie")
    
        if energie == []:
            energie = type_energie
        return energie
    
    elif user_role == "Vendeur":
        energie = st.sidebar.selectbox("Énergie", type_energie,
                                    placeholder="Choisir un type d'énergie")
        if energie != None:
            return energie
        else:
            return 'null'



# Uniquement acheteur :

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
        st.sidebar.warning("⚠️ La valeur min doit être inférieure à max !")
    st.markdown("""
    <style>
        button.step-up {display: none;}
        button.step-down {display: none;}
        div[data-baseweb] {border-radius: 4px;}
    </style>""",
    unsafe_allow_html=True)
    
    return prix_min, prix_max



def display_annee(user_role):
    try:
        annee_min, annee_max = get_plage_annee(user_role)
    except:
        annee_min, annee_max = 1928, 2024
    annee = range(annee_min, annee_max + 1, 1)
    annee_min, annee_max = st.sidebar.select_slider(
        "Année",
        options=sorted(annee),
        value=(min(annee), max(annee))
        )
    return annee_min, annee_max


# Uniquement vendeur : 

def select_annee(user_role: str, marque: str = "", modele: str = "") -> int:
    annee_min, annee_max = get_plage_annee(user_role, marque, modele)
    annee = range(annee_min, annee_max + 1, 1)
    if len(annee) == 1: 
        annee = range(annee_min-1, annee_max + 2, 1)
    annee_choisi = st.sidebar.select_slider(
        "Année",
        options=sorted(annee),
        value=max(annee)
        )
    return annee_choisi



def display_puissance():
    """
    Permet à l'utilisateur de sélectionner la puissance du véhicule. 

    ## Returns:
        int: La puissance choisie par l'utilisateur.
    """
    ch = st.sidebar.number_input("Puissance",  step=10, min_value=0, max_value=1500)
    return ch



def generation_select(choix_marque: str, choix_modele: str) -> str:
    """
    Permet à l'utilisateur de choisir la génération du véhicule en fonction de la marque et du modèle sélectionnés.

    ## Parameters:
        choix_marque (str): Marque sélectionnée.
        choix_modele (str): Modèle sélectionné.

    ## Returns:
        str: La génération sélectionnée.
    """
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
    """
    Permet à l'utilisateur de choisir le moteur du véhicule en fonction de la marque et du modèle sélectionnés.

    ## Parameters:
        choix_marque (str): Marque sélectionnée.
        choix_modele (str): Modèle sélectionné.

    ## Returns:
        str: Le moteur sélectionné.
    """
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
    """
    Permet à l'utilisateur de choisir le cylindre du véhicule en fonction de la marque et du modèle sélectionnés.

    ## Parameters:
        choix_marque (str): Marque sélectionnée.
        choix_modele (str): Modèle sélectionné.

    ## Returns:
        str: Le cyylindre sélectionné.
    """
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
    """
    Permet à l'utilisateur de choisir la finition du véhicule en fonction de la marque et du modèle sélectionnés.

    ## Parameters:
        choix_marque (str): Marque sélectionnée.
        choix_modele (str): Modèle sélectionné.

    ## Returns:
        str: La finition sélectionnée.
    """
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



def batterie_select(energie: str) -> str:
    """
    Permet à l'utilisateur de choisir la génération du véhicule en fonction du type d'énergie sélectionné.
    
    ## Parameters:
        energie (str): Type d'énergie sélectionné.

    ## Returns:
        str: La batterie sélectionnée.
    """
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
    
