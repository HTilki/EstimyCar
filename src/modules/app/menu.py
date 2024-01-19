import streamlit as st
import polars as pl
from src.modules.requetes.requetes_val_unique import get_plage_annee, get_unique_batterie, get_unique_cylindre, get_unique_finition, get_unique_generation, get_unique_marque, get_unique_modele, get_unique_moteur


def select_user_role() -> str:
    """
    Affiche une boîte de sélection dans la barre latérale pour choisir le rôle utilisateur.

    ## Returns:
        str: Le rôle sélectionné ("Acheteur" ou "Vendeur").

    ## Notes :
        Cette fonction peut être utilisée pour influencer le changement d'onglet en fonction du rôle sélectionné.
    """

    return str(st.sidebar.selectbox("Votre profil", 
                                ["Acheteur", "Vendeur"], 
                                placeholder="Choisir un profil",
                                index=None,
                                key="user_role_select"))


def display_km(user_role: str) -> tuple[int,int]|int|None:
    """
    Affiche et gère l'entrée de kilométrage en fonction du rôle de l'utilisateur.

    ## Parameters:
        user_role (str) : le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        tuple|int|None: Un tuple contenant la plage de kilométrage indiquée (km_min, km_max) ou juste le kilométrage indiqué.
    """
    if user_role == "Acheteur":
        kmmin, kmmax = st.sidebar.columns([1, 1])
        with kmmin:
            km_min = int(st.number_input("Km min", 
                                     step=10000, 
                                     min_value=0, 
                                     max_value=1000000,
                                     key="km_min_imput"))
        with kmmax:
            km_max = int(st.number_input("Km max", 
                                     step=10000, 
                                     min_value=0, 
                                     value=1000000, 
                                     max_value=1000000,
                                     key="km_max_imput"))
        if km_min > km_max:
            st.sidebar.warning("La valeur min doit être inférieure à max !", icon="⚠️")
            return None
        st.markdown("""
        <style>
            button.step-up {display: none;}
            button.step-down {display: none;}
            div[data-baseweb] {border-radius: 4px;}
        </style>""",
        unsafe_allow_html=True)
        return int(km_min), int(km_max)
    elif user_role == "Vendeur":
        km = st.sidebar.number_input("Kilométrage",  step=10000, min_value=0, max_value=1000000,
                                     key="km_input")
        return int(km)
    return None


def marques_select(nom_marques_modeles: pl.DataFrame, user_role) -> list|str|None:
    """
    Affiche une liste de marques de véhicules pour la sélection en fonction du rôle de l'utilisateur.

    ## Parameters:
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et les modèles associés des véhicules. 
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        list|str|None: Une liste des marques sélectionnées (user_role="Acheteur") ou juste la marque sélectionnée (user_role="Vendeur").
    """
    marques = get_unique_marque()

    if user_role == "Acheteur":
        choix_marques = st.sidebar.multiselect("Marque", 
                                              options=marques,
                                              placeholder="Choisir une/des marque(s)",
                                              key="marque_multiselect")
        return choix_marques
    elif user_role == "Vendeur":
        choix_marque = st.sidebar.selectbox("Marque", 
                                            options=marques,
                                            placeholder="Choisir une marque",
                                            key="marque_select")
        return choix_marque
    return None
    


def modeles_select(nom_marques_modeles: pl.DataFrame, choix_marque: list|str, user_role) -> list|str|None:
    """
    Renvoie une sélection de modèles de véhicules en fonction de la marque sélectionnée et du rôle de l'utilisateur.

    ## Parameters:
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules. 
        choix_marque (list|str): Liste ou chaine de caractères de la ou des marques sélectionnées au préalable.
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur").

    ## Returns:
        list|str|None: Une liste des modèles sélectionnés (user_role="Acheteur") ou juste le modèle sélectionné (user_role="Vendeur").
    """

    if user_role == "Acheteur":
        if not choix_marque:  # Si aucune marque n'est sélectionnée
            modeles = nom_marques_modeles.explode("modeles").to_series(1)
        else:
            modeles = nom_marques_modeles.filter(pl.col("marque").is_in(choix_marque)).explode("modeles").to_series(1)
        choix_modeles = st.sidebar.multiselect("Modèle", 
                                              options=modeles,
                                              placeholder="Choisir un/des modèle(s)",
                                              key="modele_multiselect")
        return choix_modeles
    elif user_role == "Vendeur":
        modeles = get_unique_modele(choix_marque)
        choix_modele = st.sidebar.selectbox("Modèle", 
                                            options=modeles,
                                            placeholder="Choisir un modèle",
                                            key="modele_select")
        return str(choix_modele)
    return None




def boite_select(user_role: str) -> list|str|None:
    """
    Retourne une sélection de types de boîte en fonction du rôle de l'utilisateur.

    ## Parameters:
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        list|str|None: Une liste des boites sélectionnées (user_role="Acheteur") ou juste la boite sélectionnée (user_role="Vendeur").
    """
    type_boite = pl.DataFrame(["Automatique", "Manuelle"]).to_series()
    if user_role == "Acheteur":
        boites = st.sidebar.multiselect("Boite", 
                                       options=type_boite,
                                       placeholder="Choisir un type de boite",
                                       key="boite_multiselect")
        if boites == []:
            boites = type_boite.to_list()
        return boites
    elif user_role == "Vendeur":
        boite = st.sidebar.selectbox("Boite",
                                     options=type_boite,
                                     index=None,
                                     placeholder="Choisir un type de boite",
                                     key="boite_select"
                                    )
        if boite != None:
            return str(boite)
        else:
            return 'null'
    return None
        


def energie_select(user_role: str) -> list|str|None:
    """
    Retourne une sélection de types d'énergie en fonction du rôle de l'utilisateur.

    ## Parameters:
        user_role (str): le rôle de l'utilisateur ("Acheteur" ou "Vendeur")

    ## Returns:
        list|str|None: Une liste des types d'energie sélectionnés (user_role="Acheteur") ou juste l'energie sélectionnée (user_role="Vendeur").
    """
    type_energie = pl.DataFrame([
        "Essence", 
        "Diesel",
        "Hybrides", 
        "Électrique", 
        "Bicarburation essence bioéthanol", 
        "Bicarburation essence / gpl"]).to_series()
    if user_role == "Acheteur":
        energies = st.sidebar.multiselect("Énergie", 
                                         options=type_energie,
                                         placeholder="Choisir un type d'énergie",
                                         key="energie_multiselect")
        if energies == []:
            energies = type_energie.to_list()
        return energies    
    elif user_role == "Vendeur":
        energie = st.sidebar.selectbox("Énergie", 
                                       options=type_energie,
                                       index=None,
                                       placeholder="Choisir un type d'énergie",
                                       key="energie_select")
        if energie != None:
            return str(energie)
        else:
            return 'null'
    return None

def display_prix_selection() -> tuple:
    """
    Affiche des champs de saisie pour sélectionner un prix minimal et maximal.

    ## Returns:
        tuple: Un tuple contenant le prix minimum et maximum indiqués par l'utilisateur.
    """

    prixmin, prixmax = st.sidebar.columns([1, 1])
    with prixmin:
        prix_min = st.number_input("Prix min",  step=1000, min_value=0, max_value=3000000)
    with prixmax:
        prix_max = st.number_input("Prix max", step=1000, min_value=0, value=3000000, max_value=3000000)
    if prix_min > prix_max:
        st.sidebar.warning("La valeur min doit être inférieure à max !", icon="⚠️")
    st.markdown("""
                <style>
                    button.step-up {display: none;}
                    button.step-down {display: none;}
                    div[data-baseweb] {border-radius: 4px;}
                </style>""",
    unsafe_allow_html=True)
    return prix_min, prix_max


def display_annee(user_role: str, marque: str = "", modele: str = "") -> tuple|int:
    """
    Affiche un sélecteur d'année dans la barre latérale.

    ## Parameters:
        user_role (str): Le rôle de l'utilisateur
        marque (str, optional): Le nom de la marque de voiture. Defaults to None.
        modele (str, optional): Le nom du modèle de voiture. Defaults to None.

    ## Returns:
        tuple|int: Un tuple contenant la plage d'années sélectionnée (année_min, année_max) ou juste l'année selectionnée.
    """
    if user_role == "Acheteur":
        annee_min, annee_max = get_plage_annee(user_role)
        annee = list(range(annee_min, annee_max + 1, 1))
        annee_choisi = tuple(st.sidebar.select_slider(
            "Année",
            options=pl.DataFrame(annee).to_series(),
            value=(annee_min, annee_max),
            key="annee_double_slider"
            ))
    elif user_role == "Vendeur":
        annee_min, annee_max = get_plage_annee(user_role, marque, modele)
        annee = list(range(annee_min, annee_max + 1, 1))
        if len(annee) == 1: 
            annee = list(range(annee_min-1, annee_max + 2, 1))
        annee_choisi = st.sidebar.select_slider(
            "Année",
            options=pl.DataFrame(annee).to_series(),
            value=annee_max,
            key="annee_single_slider"
            )
    return annee_choisi



def display_puissance() -> int:
    """
    Permet à l'utilisateur de sélectionner la puissance du véhicule. 

    ## Returns:
        int: La puissance choisie par l'utilisateur.
    """
    ch = st.sidebar.number_input("Puissance", step=10, min_value=0, max_value=1500, key="puissance_input")
    return int(ch)



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
                                        placeholder="Choisir la génération",
                                        key="generation_select")
    if choix_generation == "Autre choix...": 
        choix_generation_2 = st.sidebar.text_input("Autre choix de génération",
                                            placeholder="Saisissez la génération",
                                            key="generation_input")
        return choix_generation_2
    elif choix_generation == None: 
        return 'null'
    else:
        return str(choix_generation)
    


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
                                        placeholder="Choisir un moteur",
                                        key="moteur_select")
    if choix_moteur == "Autre choix...": 
        choix_moteur_2 = st.sidebar.text_input("Autre choix de moteur",
                                            placeholder="Saisissez votre moteur",
                                            key="moteur_input")
        return choix_moteur_2
    elif choix_moteur == None: 
        return 'null'
    else : 
        return str(choix_moteur)



def cylindre_select(choix_marque: str, choix_modele: str) -> str:
    """
    Permet à l'utilisateur de choisir le cylindre du véhicule en fonction de la marque et du modèle sélectionnés.

    ## Parameters:
        choix_marque (str): Marque sélectionnée.
        choix_modele (str): Modèle sélectionné.

    ## Returns:
        str: Le cylindre sélectionné.
    """
    cylindres = get_unique_cylindre(choix_marque, choix_modele) + ["Autre choix..."]
    choix_cylindre = st.sidebar.selectbox("Cylindre", cylindres,
                                        index=None,
                                        placeholder="Choisir un cylindre",
                                        key="cylindre_select")
    if choix_cylindre == "Autre choix...": 
        choix_cylindre_2 = st.sidebar.text_input("Autre choix de cylindre",
                                            placeholder="Exemple: 4.0",
                                            key="cylindre_input")
        return choix_cylindre_2
    elif choix_cylindre == None: 
        return 'null'
    else : 
        return str(choix_cylindre)
    

    
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
                                        placeholder="Choisir une finition",
                                        key="finition_select")
    if choix_finition == "Autre choix...": 
        choix_finition_2 = st.sidebar.text_input("Autre choix de finition",
                                            placeholder="Choisir une finition",
                                            key="finition_input")
        return choix_finition_2
    elif choix_finition == None: 
        return 'null'
    else : 
        return str(choix_finition)



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
                                            placeholder="Choisir une autonomie",
                                            key="batterie_select")
        if choix_batterie == "Autre choix...": 
            choix_batterie_2 = st.sidebar.text_input("Autre choix de batterie",
                                                placeholder="Exemple: 100kWh",
                                                key="batterie_input")
            return choix_batterie_2
        else: 
            return str(choix_batterie)
    else:
        return 'null'