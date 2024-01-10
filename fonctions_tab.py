import streamlit as st
from requetes_dataframe import get_dataframe
from machinelearning import predict_prix, predict_prix_autre_km
from numpy import ndarray
import polars as pl

def show_dataframe(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int):
    """
    Affiche un DataFrame Pandas basé sur les critères spécifiés, avec des options de personnalisation.

    ## Parameters:
        marques (list): Liste de noms de marques à filtrer. Si vide, aucune restriction par marque.
        modeles (list): Liste de noms de modèles à filtrer. Si vide, aucune restriction par modèle.
        annee_min (int): Année minimale des véhicules à inclure dans le filtre.
        annee_max (int): Année maximale des véhicules à inclure dans le filtre.
        km_min (int): Kilométrage minimal des véhicules à inclure dans le filtre.
        km_max (int): Kilométrage maximal des véhicules à inclure dans le filtre.
        boite (list): Liste de types de boîtes de vitesses à inclure dans le filtre.
        energie (list): Liste de types d'énergie à inclure dans le filtre.
        prix_min (int): Prix minimal des véhicules à inclure dans le filtre.
        prix_max (int): Prix maximal des véhicules à inclure dans le filtre.
    
    ## Returns:
        None: Affiche un DataFrame interactif dans l'interface utilisateur avec les annonces correspondant aux critères spécifiés. En cas d'erreur ou d'absence d'annonces, affiche un message approprié.
    """

    try:
        st.dataframe(get_dataframe(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max), 
                            width=20000,
                            height=600,
                            column_config={
                                'annee': st.column_config.NumberColumn(
                                    "Année 📅",
                                    format="%d"
                                    ),
                                    'prix': st.column_config.NumberColumn(
                                        "Prix 💰 (en euros)",
                                        format="%d €"
                                        ),
                                        'lien': st.column_config.LinkColumn(
                                            "Lien 🔗"
                                        ),
                                        'energie': st.column_config.TextColumn(
                                            "Énergie ⚡️"
                                        ),
                                        'boite': st.column_config.TextColumn(
                                            "Boîte 🛠️"
                                        ),
                                        'cylindre': st.column_config.NumberColumn(
                                            "Cylindre 🛢️"
                                        ),
                                        'puissance': st.column_config.NumberColumn(
                                            "Puissance 💥"
                                        ),
                                        'moteur': st.column_config.TextColumn(
                                            "Moteur 🐎"
                                        ),
                                        'Véhicule': st.column_config.TextColumn(
                                            "Véhicule 🚘"
                                        ),
                                        'Position_marché' : st.column_config.TextColumn(
                                            "Position Marché ⚖️"
                                        )

                                    }
                                    )
    except:
        st.write("Aucune annonce ne correspond à la description donnée.")



def predict_button(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str):
    """
    Crée un bouton interactif pour estimer la valeur d'un véhicule en fonction des paramètres spécifiés.

    ## Parameters:
        marque (str): Marque du véhicule.
        modele (str): Modèle du véhicule.
        annee (int): Année de fabrication du véhicule.
        moteur (str): Type de moteur du véhicule.
        cylindre (str): Cylindrée du moteur du véhicule.
        puissance (int): Puissance du moteur en chevaux.
        km (int): Kilométrage du véhicule.
        boite (str): Type de boîte de vitesses du véhicule.
        energie (str): Type d'énergie du véhicule.
        batterie (str): Type de batterie pour les véhicules électriques.
        generation (str): Génération du modèle de véhicule.
        finition (str): Finition du véhicule.

    ## Returns:
        None: Affiche le résultat de la prédiction du prix dans l'interface utilisateur lorsqu'on appuie sur le bouton. En cas d'erreur, aucun résultat n'est affiché.
    """

    if st.button('Estimer la valeur du véhicule.'):
        data = transform_input(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
        st.write('Prix estimé : ', format_prediction(predict_prix(data, marque)))

def transform_input(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str) -> pl.DataFrame:
    """
    Transforme les paramètres d'un véhicule en un DataFrame pour être utilisé dans le modèle de prédiction.

    ## Parameters:
        marque (str): Marque du véhicule.
        modele (str): Modèle du véhicule.
        annee (int): Année de fabrication du véhicule.
        moteur (str): Type de moteur du véhicule.
        cylindre (str): Cylindrée du moteur du véhicule.
        puissance (int): Puissance du moteur en chevaux.
        km (int): Kilométrage du véhicule.
        boite (str): Type de boîte de vitesses du véhicule.
        energie (str): Type d'énergie du véhicule.
        batterie (str): Type de batterie pour les véhicules électriques.
        generation (str): Génération du modèle de véhicule.
        finition (str): Finition du véhicule.

    ## Returns:
        pl.DataFrame: DataFrame contenant les paramètres du véhicule transformés pour la prédiction.
    """

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
    """
    Formate la prédiction du prix en tant que chaîne de caractères.

    ## Parameters:
        prix_predit (numpy.ndarray): Matrice contenant le prix prédit.

    ## Returns:
        str: Prix prédit formaté en euros.
    """
    return str(prix_predit[0, 0]) + ' €' 


def predict_km_fictif_button(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str):
    """
    Bouton pour estimer la valeur d'un véhicule en fonction de kilométrage fictif.

    ## Parameters:
        marque (str): Marque du véhicule.
        modele (str): Modèle du véhicule.
        annee (int): Année du véhicule.
        moteur (str): Type de moteur du véhicule.
        cylindre (str): Cylindrée du moteur du véhicule.
        puissance (int): Puissance du moteur du véhicule.
        km (int): Kilométrage réel du véhicule.
        boite (str): Type de boîte de vitesses du véhicule.
        energie (str): Type d'énergie du véhicule.
        batterie (str): Type de batterie du véhicule.
        generation (str): Génération du véhicule.
        finition (str): Finition du véhicule.

    ## Displays:
        Affiche un graphique interactif pour estimer la valeur du véhicule en fonction de kilométrage fictif.
    """
    if st.button('Estimer la valeur de votre véhicule selon le kilométrage.'):
        data = transform_input(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
        fig = predict_prix_autre_km(data, marque)
        st.plotly_chart(fig)


