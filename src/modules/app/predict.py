import polars as pl
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.compose import ColumnTransformer
from joblib import load
import numpy as np
import plotly.express as px
import plotly.graph_objects as Figure


def charger_modeles(
    marque: str,
) -> tuple[
    LinearRegression | KNeighborsRegressor | RandomForestRegressor, ColumnTransformer
]:
    """
    Charge le modèle de régression et le préprocesseur associé pour une marque donnée.

    ## Parameters:
        marque (str): Nom de la marque pour laquelle le modèle est chargé.

    ## Returns:
        tuple[LinearRegression | KNeighborsRegressor | RandomForestRegressor, ColumnTransformer]: Le modèle chargé.

    ## Example:
        >>> model, preprocessor = charger_modeles('PORSCHE')
        # Charge le modèle de régression et le préprocesseur associé pour la marque PORSCHE.
    """
    try:
        model = load(f"src/models/{marque.upper()}_best_model.joblib")
        preprocessor = load(f"src/models/{marque.upper()}_preprocessor.joblib")
    except Exception as e:
        print(f"Erreur lors de l'importation du modèle : {str(e)}")
    return model, preprocessor


def predict_prix(data: pl.DataFrame, marque: str) -> float | None:
    """
    Prédit les prix des véhicules pour une marque donnée en utilisant le modèle chargé.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules à prédire.
        marque (str): Nom de la marque pour laquelle les prix sont prédits.

    ## Returns:
        float: La prédictions du prix.

    ## Example:
        >>> predict_prix(data_to_predict, 'PORSCHE')
        # Prédit les prix des véhicules pour la marque PORSCHE en utilisant le modèle chargé.

    Raises:
        Exception: En cas d'erreur lors de la prédiction du prix.
    """
    try:
        modele, preprocessor = charger_modeles(marque.upper())
        prediction = modele.predict(preprocessor.transform(data.to_pandas()))
        prediction = np.round(prediction, decimals=2)
        if isinstance(modele, LinearRegression | KNeighborsRegressor):
            if len(data) == 1:
                return prediction[0][0]
            else:
                return prediction.flatten()
        elif isinstance(modele, RandomForestRegressor):
            if len(data) == 1:
                return prediction[0]
            else:
                return prediction.flatten()
    except Exception as e:
        print(f"Erreur lors de la prédiction du prix. {e}")
    return None


def predict_prix_autre_km(data: pl.DataFrame, marque: str) -> Figure:
    """
    Prédit les prix des véhicules pour une marque donnée en utilisant le modèle chargé, en simulant différents kilométrages.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules d'origine.
        marque (str): Nom de la marque pour laquelle les prix sont prédits.

    ## Returns:
        Figure: le graphique plotly.

    ## Example:
        >>> predict_prix_autre_km(data_origine, 'PORSCHE')
        # Prédit les prix des véhicules pour la marque PORSCHE en utilisant le modèle chargé,
        # en simulant différents kilométrages.
    """
    data_fictif = data.with_columns(type_km=pl.lit("Kilométrage fictif"))
    data = data.with_columns(type_km=pl.lit("Kilométrage aujourd'hui"))

    for i in range(0, 310000, 10000):
        data = pl.concat(
            [
                data,
                data_fictif.with_columns(kilometrage=i).cast({"kilometrage": pl.Int64}),
            ]
        )

    prix_predit = predict_prix(data.drop("type_km"), marque.upper())

    data = data.with_columns(pl.Series(name="Prix estimé", values=prix_predit)).sort(
        "kilometrage"
    )

    fig = px.line(
        data,
        x="kilometrage",
        y="Prix estimé",
        title="Prix estimé en fonction du kilométrage du véhicule",
        markers=True,
        color="type_km",
    )
    fig.update_layout(legend_title_text=None)
    fig.update_layout(xaxis=dict(tickformat="d"), yaxis=dict(tickformat="d"))
    return fig
