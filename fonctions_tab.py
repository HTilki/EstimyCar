import streamlit as st
from requetes_dataframe import get_dataframe
from machinelearning import predict_prix, predict_prix_autre_km
from numpy import ndarray
import polars as pl

def show_dataframe(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int):

    try:
        st.dataframe(get_dataframe(marques, modeles, annee_min, annee_max, km_min, km_max, boite, energie, prix_min, prix_max), 
                            width=20000,
                            height=600,
                            column_config={
                                'annee': st.column_config.NumberColumn(
                                    format="%d"
                                    ),
                                    'prix': st.column_config.NumberColumn(
                                        "Prix (en euros)",
                                        format="%d €"
                                        ),
                                        'lien': st.column_config.LinkColumn(
                                            "Lien"
                                        )
                                    }
                                    )
    except:
        st.write("Aucune annonce ne correspond à la description donnée.")



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
