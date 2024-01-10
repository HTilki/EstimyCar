import duckdb
import polars as pl
import plotly.express as px
import streamlit as st

def get_avg_price_by_brand():
    """
    Affiche un barplot représentant le prix moyen par marque de véhicule.
    """
    prix_moyen_m = duckdb.sql(
        f"""
        SELECT marque, AVG(prix) AS prix_moyen
        FROM 'data/database.parquet'
        GROUP BY marque
        ORDER BY prix_moyen DESC
        """).df()
    
    fig = px.bar(prix_moyen_m, x="marque", y="prix_moyen", title="Prix moyen par marque", color= "prix_moyen",
                color_continuous_scale='YlOrRd')
    fig.update_xaxes(title="Marque")
    fig.update_yaxes(title="Prix moyen")
    fig.update_coloraxes(showscale=False) 
    st.plotly_chart(fig, use_container_width=True, height=600)


def get_price_histogram():
    """
    Affiche un histogramme représentant la distribution des prix des véhicules compris entre 0 et 150 000€.
    """
    prices = duckdb.sql(
        f"""
        SELECT prix
        FROM 'data/database.parquet'
        WHERE prix BETWEEN 0 AND 150000
        """).df()

    fig = px.histogram(prices, x= "prix", nbins=30, title= "Distribution des prix des véhicules")
    fig.update_xaxes(title= "Prix")
    fig.update_traces(marker=dict(color='#d62728', opacity=0.7))
    fig.update_yaxes(title= "Nombre de voitures")
    st.plotly_chart(fig, use_container_width=True, height=600)


def get_count_models_by_brand():
    """
    Affiche un barplot indiquant le nombre de modèles par marque de véhicule.
    """
    count_models = duckdb.sql(
        f"""
        SELECT marque, COUNT(DISTINCT modele) AS nombre_modeles
        FROM 'data/database.parquet'
        GROUP BY marque
        ORDER BY nombre_modeles DESC
        """).df()
    
    fig = px.bar(count_models, x="marque", y="nombre_modeles", title="Nombre de modèles par marque", color="nombre_modeles", 
                color_continuous_scale='Reds')
    fig.update_xaxes(title="Marque")
    fig.update_yaxes(title="Nombre de modèles")
    fig.update_coloraxes(showscale=False) 
    st.plotly_chart(fig, use_container_width=True, height=600)



def show_selected_chart():
    """
    Permet à l'utilisateur d'afficher différents types de graphiques liés aux données des véhicules.
    """
    selected_chart = st.selectbox("Choisir le graphique à afficher", 
                                        ("Nombre de modèles par marque", 
                                        "Prix moyen par marque", 
                                        "Histogramme des prix"))

    if selected_chart == "Nombre de modèles par marque":
        model_brand = get_count_models_by_brand()

    elif selected_chart == "Prix moyen par marque":
        prix_moyen = get_avg_price_by_brand()

    elif selected_chart == "Histogramme des prix":
        st.markdown("Distribution des prix des véhicules entre `0`  et  `150 000 `€")
        price = get_price_histogram()
