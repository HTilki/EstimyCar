import streamlit as st
from requete_dataframe import get_dataframe

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