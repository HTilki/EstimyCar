import streamlit as st
from src.modules.requetes.requetes_dataframe import get_dataframe
from src.modules.requetes.requetes_kpi import get_avg_price
from src.modules.app.predict import predict_prix, predict_prix_autre_km
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
                                            "Puissance 🐎"
                                        ),
                                        'kilometrage': st.column_config.NumberColumn(
                                            "Kilométrage ⚙️"
                                        ),
                                        'moteur': st.column_config.TextColumn(
                                            "Moteur 💥"
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



def predict_button(marque: str, modele: str, annee: int, moteur: str, cylindre: str, puissance: int, km: int, boite: str, energie: str, batterie: str, generation: str, finition: str, user_role: str = 'Vendeur'):
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
        user_role (str): 'Vendeur' par défaut, le type d'utilisateur .

    ## Returns:
        None: Affiche le résultat de la prédiction du prix dans l'interface utilisateur lorsqu'on appuie sur le bouton. En cas d'erreur, aucun résultat n'est affiché.
    """

    if st.button('**Estimer la valeur du véhicule.**',
                 key="predict_button"):
        data = transform_input(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
        prix_pred = predict_prix(data, marque)
        prix_moyen = get_avg_price(marque, modele, 0, annee, 0, km, boite, energie, 0, 0, user_role, cylindre, puissance)
        st.session_state['prix_pred'] = prix_pred
        st.session_state['prix_moy_pred'] = prix_moyen

def get_prix_pred_displayed() -> None:
    """
    Affiche le prix estimé dans l'interface Streamlit.

    ## Notes:
        Cette fonction vérifie si le prix estimé est disponible dans la session Streamlit.
        Si oui, elle affiche le prix estimé.
        Sinon, elle affiche un message d'erreur.
    """
    if 'prix_pred' in st.session_state:
        if st.session_state['prix_pred'] != None:
            st.metric('**:orange[Prix estimé :]** ', value=format_prix(st.session_state['prix_pred']))
        else : 
            st.metric('**:red[Prix estimé :]** ', value="Erreur lors de l'estimation du prix.")
            
def get_prix_moy_displayed() -> None:
    """
    Affiche le prix moyen dans l'interface Streamlit.

    ## Notes:
        Cette fonction vérifie si le prix moyen est disponible dans la session Streamlit.
        Si oui, elle affiche le prix moyen et fournit une aide contextuelle.
        Sinon, elle affiche un message indiquant que le prix moyen est indisponible avec une aide contextuelle.
    """
    if 'prix_moy_pred' in st.session_state:
        if st.session_state['prix_moy_pred'] != 0:
            st.metric('**:blue[Prix moyen :]** ', value=format_prix(st.session_state['prix_moy_pred']),
                      help="Ce prix est calculé par rapport à la marque, le modèle, l'année, l'energie, la boite, la cylindre, la puissance ± 10, le kilométrage ± 3000.")
        else:
            st.metric('**:red[Prix moyen :]** ', value="Prix moyen indisponible.",
                      help = "Le prix moyen n'a pas pu être calculé car il n'y a pas de véhicule avec les mêmes caractéristiques renseignées dans notre base de données.")

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

def format_prix(prix: float) -> str:
    """
    Formate le prix en tant que chaîne de caractères.

    ## Parameters:
        prix (float): Le prix.

    ## Returns:
        str: Prix formaté en euros.
    """
    return str(prix) + ' €' 


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
    if st.button("**Estimer la valeur de votre véhicule selon le kilométrage.**",
                 key="predict_km_plot_button"):
        try:
            data = transform_input(marque, modele, annee, moteur, cylindre, puissance, km, boite, energie, batterie, generation, finition)
            fig = predict_prix_autre_km(data, marque)
            st.plotly_chart(fig, use_container_width=True, height=600)
        except:
            st.error("Erreur lors de la génération du graphique. Vérifiez que toutes les caractéristiques sont bien renseignées.")

