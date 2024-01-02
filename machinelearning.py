"""
Module de prédiction de prix de véhicules.

Ce module contient des fonctions pour l'entraînement de modèles de régression, la prédiction des prix de véhicules,
et la gestion des modèles sauvegardés.

"""

import polars as pl
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as Figure
import warnings
from sklearn.base import RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from joblib import dump, load

def split_data(data: pl.DataFrame, marque: str) -> tuple[pl.DataFrame, pl.DataFrame, pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Sépare les données en ensembles d'entraînement et de test pour une marque spécifique.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules.
        marque (str): Nom de la marque pour laquelle les données doivent être séparées.

    ## Returns:
        - X (pl.DataFrame): DataFrame des features pour la marque spécifiée, excluant les colonnes 'position_marché', 'lien', 'garantie', et 'prix'.
        - y (pl.DataFrame): DataFrame de la cible (prix) correspondant à la marque spécifiée.
        - X_train (pd.DataFrame): DataFrame d'entraînement des features au format pandas.
        - X_test (pd.DataFrame): DataFrame de test des features au format pandas.
        - y_train (np.ndarray): Array numpy d'entraînement de la cible.
        - y_test (np.ndarray): Array numpy de test de la cible.

    ## Notes:
        Les colonnes 'position_marché', 'lien', 'garantie' et 'prix' sont exclues des features.

    """
    X = data.filter(pl.col("marque") == marque)
    y = X.select('prix')
    X = X.select(pl.exclude("position_marché")
                 ).select(pl.exclude("lien")
                          ).select(pl.exclude("garantie")
                                   ).select(pl.exclude("prix"))

    # Split des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X.to_pandas(), y.to_numpy(), test_size=0.2, random_state=21)
    return X, y, X_train, X_test, y_train, y_test

def get_preprocessor() -> ColumnTransformer:
    """
    Retourne un transformateur de colonnes scikit-learn (ColumnTransformer) pour prétraiter les caractéristiques numériques et catégorielles.

    Les caractéristiques numériques ('annee', 'kilometrage', 'puissance') sont mises à l'échelle à l'aide de StandardScaler,
    et les caractéristiques catégorielles ('boite', 'cylindre', 'energie', 'marque', 'modele', 'generation', 'moteur', 'finition', 'batterie')
    sont encodées en one-hot à l'aide de OneHotEncoder avec gestion des catégories inconnues.

    ## Returns:
        ColumnTransformer: Un transformateur de colonnes scikit-learn pour prétraiter les caractéristiques numériques et catégorielles.

    ## Example:
        >>> preprocessor = get_preprocessor()
        >>> # En supposant que 'data' est une DataFrame avec les caractéristiques spécifiées
        >>> data_transformee = preprocessor.fit_transform(data) 
    """
    numeric_features = ['annee', 'kilometrage', 'puissance']
    categorical_features = ['boite', 'cylindre', 'energie', 'marque', 'modele', 'generation', 'moteur', 'finition', 'batterie']

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor

def set_models() -> tuple[dict, dict]:
    """
    Définit les modèles de régression et les grilles de paramètres associées pour la recherche sur grille.

    ## Returns:
        tuple[dict, dict]: Un tuple contenant un dictionnaire de modèles (models) et un dictionnaire de grilles de paramètres (param_grids).

    Modèles disponibles :
    - 'LinearRegression': Régression linéaire
    - 'KNeighbors': Régression des k plus proches voisins
    - 'RandomForest': Forêt aléatoire

    Grilles de paramètres pour la recherche sur grille :
    - 'LinearRegression': Aucun paramètre spécifié.
    - 'KNeighbors':
        - 'n_neighbors': [1, 3, 5, 7]
        - 'weights': ['uniform', 'distance']
    - 'RandomForest':
        - 'n_estimators': [50, 100, 200]
        # Autres paramètres commentés pour simplifier, à décommenter au besoin
        # - 'max_depth': [None, 10, 20]
        # - 'min_samples_split': [2, 5, 10]
        # - 'min_samples_leaf': [1, 2, 4]

    ## Example:
        >>> models, param_grids = set_models()
        >>> # Utilisation des modèles et grilles de paramètres dans un processus de recherche sur grille
    """

    # Modèles
    models = {
        'LinearRegression': LinearRegression(),
        'KNeighbors': KNeighborsRegressor(),
        'RandomForest': RandomForestRegressor(n_jobs=-1)
    }

    # Paramètres pour la recherche sur grille
    param_grids = {
        'LinearRegression': {},
        'KNeighbors': {
            'n_neighbors': [1, 3, 5, 7],
            'weights': ['uniform', 'distance']
        },
        'RandomForest': {
            'n_estimators': [50, 100, 200],
            #'max_depth': [None, 10, 20],
            #'min_samples_split': [2, 5, 10],
            #'min_samples_leaf': [1, 2, 4]
        }
    }
    return models, param_grids

def find_best_model(models: dict, param_grids: dict, preprocessor: ColumnTransformer, X_train: pd.DataFrame, y_train: np.ndarray, marque: str) -> tuple[LinearRegression|KNeighborsRegressor|RandomForestRegressor, str]:
    """
    Recherche et retourne le meilleur modèle de régression pour une marque donnée en utilisant la validation croisée.

    ## Parameters:
        models (dict): Dictionnaire des modèles de régression à évaluer.
        param_grids (dict): Dictionnaire des grilles de paramètres associées aux modèles.
        preprocessor (ColumnTransformer): Transformateur de colonnes utilisé pour prétraiter les données.
        X_train (pd.DataFrame): DataFrame d'entraînement des features.
        y_train (np.ndarray): Array numpy d'entraînement de la cible.
        marque (str): Nom de la marque pour laquelle le meilleur modèle est recherché.

    ## Returns:
        tuple[LinearRegression | KNeighborsRegressor | RandomForestRegressor, str]:
        Un tuple contenant le meilleur modèle sélectionné et le nom du modèle.

    ## Example:
        >>> models, param_grids = set_models()
        >>> best_model, best_model_name = find_best_model(models, param_grids, preprocessor, X_train, y_train, 'CITROEN')
        >>> # Utilisation du meilleur modèle dans la suite de l'analyse

    ## Notes:
        Les résultats de la recherche sur grille sont exportés dans un fichier JSON dans le répertoire 'cv_results'
        sous le format "{marque}_{model_name}_results.json".
    """
    best_score = float('-inf')

    for model_name, model in models.items():
        # Recherche sur grille avec validation croisée
        grid_search = GridSearchCV(model, param_grids[model_name], cv=5)
        grid_search.fit(preprocessor.fit_transform(X_train), y_train)

        # Stocker les résultats de la recherche sur grille dans un DataFrame ou un dictionnaire
        results = pd.DataFrame(grid_search.cv_results_).sort_values(by="rank_test_score").head(5)
        
        # Exporter les résultats dans un fichier JSON
        results.to_json(f'cv_results/{marque}_{model_name}_results.json', orient='records', lines=True)

        # Mettre à jour le meilleur modèle si nécessaire
        if grid_search.best_score_ > best_score:
            best_score = grid_search.best_score_
            best_model = grid_search.best_estimator_
            best_model_name = model_name

    return best_model, best_model_name


def print_best_results(marque: str, best_model_name: str, best_model: LinearRegression|KNeighborsRegressor|RandomForestRegressor, mae: float) -> None:
    """
    Affiche les résultats du meilleur modèle de régression pour une marque donnée.

    ## Parameters:
        marque (str): Nom de la marque pour laquelle les résultats sont affichés.
        best_model_name (str): Nom du meilleur modèle sélectionné.
        best_model (LinearRegression | KNeighborsRegressor | RandomForestRegressor): Instance du meilleur modèle sélectionné.
        mae (float): Erreur Moyenne Absolue (MAE) sur l'ensemble de test.

    ## Returns:
        None

    ## Example:
        >>> print_best_results('PORSCHE', 'KNeighbors', KNeighborsRegressor(algorithm='auto',..., n_neighbors=3, p=2, weights='distance'), 8737.218)
        --- PORSCHE ---
        Meilleur modèle : KNeighbors
        Paramètres du meilleur modèle : {'algorithm': 'auto', ..., 'n_neighbors': 3, 'p': 2, 'weights': 'distance'}
        Erreur Moyenne Absolue (MAE) sur l'ensemble de test : 8737.218
    """
    # Print des résultats
    print(f"--- {marque} ---")
    print(f"Meilleur modèle : {best_model_name}")
    print(f"Paramètres du meilleur modèle : {best_model.get_params()}")
    print(f"Erreur Moyenne Absolue (MAE) sur l'ensemble de test : {mae}")

def export_models(model: LinearRegression|KNeighborsRegressor|RandomForestRegressor, preprocessor: ColumnTransformer, marque: str) -> None:    
    """
    Exporte le modèle de régression et le préprocesseur associé pour une marque donnée.

    ## Parameters:
        model (Union[LinearRegression, KNeighborsRegressor, RandomForestRegressor]): Modèle de régression à exporter.
        preprocessor (ColumnTransformer): Préprocesseur associé au modèle.
        marque (str): Nom de la marque pour laquelle le modèle est exporté.

    ## Returns:
        None

    ## Example:
        >>> export_models(KNeighborsRegressor(), preprocessor, 'PORSCHE')
        # Exporte le modèle KNeighborsRegressor et le préprocesseur associé pour la marque PORSCHE.
        # Les fichiers sont sauvegardés dans le répertoire 'models'.

    ## Notes:
        Les fichiers sont sauvegardés dans le répertoire 'models' avec les noms '{marque}_best_model.joblib'
        et '{marque}_preprocessor.joblib'.
    """ 
    # Sauvegarder le modèle
    dump(model, f'models/{marque}_best_model.joblib')
    # Sauvegarder le préprocesseur
    dump(preprocessor, f'models/{marque}_preprocessor.joblib')

def preprocess_train_and_evaluate_model(data: pl.DataFrame, marque: str) -> None:
    """
    Préprocesse les données, entraîne et évalue le meilleur modèle de régression pour une marque donnée.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules.
        marque (str): Nom de la marque pour laquelle le modèle est entraîné et évalué.

    ## Returns:
        None

    ## Example:
        >>> preprocess_train_and_evaluate_model(data, 'PORSCHE')
        # Préprocesse les données, entraîne et évalue le meilleur modèle pour la marque PORSCHE.
        # Les résultats, le meilleur modèle et le préprocesseur associé sont exportés.

    ## Notes:
        Les résultats de la recherche sur grille et les informations du meilleur modèle sont exportés
        dans le répertoire 'cv_results' avec les noms '{marque}_{model_name}_results.json'.
        Le meilleur modèle et le préprocesseur associé sont sauvegardés dans le répertoire 'models' avec les noms '{marque}_best_model.joblib'
        et '{marque}_preprocessor.joblib'.
    """
    #split
    X, y, X_train, X_test, y_train, y_test = split_data(data, marque)

    # Préprocesseur
    preprocessor = get_preprocessor()
    
    models, param_grids = set_models()
    
    # trouver le meilleur modele
    best_model, best_model_name = find_best_model(models, param_grids, preprocessor, X_train, y_train, marque)

    # Test sur l'ensemble de test
    y_pred = best_model.predict(preprocessor.transform(X_test))
    
    # entrainement sur tout le dataset
    best_model.fit(preprocessor.fit_transform(X.to_pandas()), y.to_numpy())
    preprocessor.fit(X.to_pandas())

    # Calcul de l'erreur moyenne absolue (MAE)
    mae = mean_absolute_error(y_test, y_pred)

    print_best_results(marque, best_model_name, best_model, mae)

    export_models(best_model, preprocessor, marque)


def get_all_models(data: pl.DataFrame, nom_marques_modeles: pl.DataFrame) -> None :
    """
    Entraîne et évalue tous les modèles de régression pour chaque marque présente dans le DataFrame 'nom_marques_modeles'.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules.
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et les modèles associés des véhicules.

    ## Returns:
        None

    ## Example:
        >>> get_all_models(data, nom_marques_modeles)
        # Entraîne et évalue tous les modèles de régression pour chaque marque dans le DataFrame 'nom_marques_modeles'.
        # Les résultats sont exportés pour chaque modèle.

    ## Notes:
        Les résultats de la recherche sur grille et les informations des meilleurs modèles sont exportés
        dans le répertoire 'cv_results' avec les noms '{marque}_{model_name}_results.json'
        et '{marque}_best_model.joblib' respectivement.
    """
    warnings.filterwarnings("ignore")
    for marque in nom_marques_modeles['marque'].to_numpy():
        preprocess_train_and_evaluate_model(data, marque)

def charger_modeles(marque: str) -> tuple[LinearRegression|KNeighborsRegressor|RandomForestRegressor, ColumnTransformer]:
    """
    Charge le modèle de régression et le préprocesseur associé pour une marque donnée.

    ## Parameters:
        marque (str): Nom de la marque pour laquelle le modèle est chargé.

    ## Returns:
        tuple[LinearRegression | KNeighborsRegressor | RandomForestRegressor, ColumnTransformer]

    ## Example:
        >>> model, preprocessor = charger_modeles('PORSCHE')
        # Charge le modèle de régression et le préprocesseur associé pour la marque PORSCHE.
    """    
    try:
        model = load(f"models/{marque}_best_model.joblib")
        preprocessor = load(f"models/{marque}_preprocessor.joblib")
        return model, preprocessor
    except Exception as e:
        print(f"Erreur lors de l'importation du modèle : {str(e)}")
        

def predict_prix(data: pl.DataFrame, marque: str) -> np.ndarray:
    """
    Prédit les prix des véhicules pour une marque donnée en utilisant le modèle chargé.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules à prédire.
        marque (str): Nom de la marque pour laquelle les prix sont prédits.

    ## Returns:
        np.ndarray: Tableau NumPy contenant les prédictions de prix.

    ## Example:
        >>> predict_prix(data_to_predict, 'PORSCHE')
        # Prédit les prix des véhicules pour la marque PORSCHE en utilisant le modèle chargé.

    Raises:
        Exception: En cas d'erreur lors de la prédiction du prix.
    """
    try:
        modele, preprocessor = charger_modeles(marque)
        prediction = modele.predict(preprocessor.transform(data.to_pandas()))
        prediction = np.round(prediction, decimals=2)
        return prediction
    except Exception as e:
        print(f"Erreur lors de la prédiction du prix. {e}")

def predict_prix_autre_km(data: pl.DataFrame, marque: str) -> Figure:
    """
    Prédit les prix des véhicules pour une marque donnée en utilisant le modèle chargé, en simulant différents kilométrages.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les données des véhicules d'origine.
        marque (str): Nom de la marque pour laquelle les prix sont prédits.

    ## Returns:
        Figure: Objet Figure de Plotly contenant le graphique interactif des prédictions de prix. 

    ## Example:
        >>> predict_prix_autre_km(data_origine, marque)
        # Prédit les prix du véhicule de la marque en utilisant le modèle chargé,
        # en simulant différents kilométrages.
    """
    data_fictif = data.with_columns(type_km=pl.lit("Kilométrage fictif"))
    data = data.with_columns(type_km=pl.lit("Kilométrage aujourd'hui"))

    for i in range(0, 310000, 10000):
        data = pl.concat([data,
                          data_fictif.with_columns(kilometrage=i).cast({"kilometrage": pl.Int64})])

    prix_predit = predict_prix(data.drop('type_km'), marque)

    data = data.with_columns(
        pl.Series(name='Prix estimé', values=prix_predit)
    ).sort(
        "kilometrage"
    ).with_columns(
        pl.col("Prix estimé").map_batches(_convert_list_float).alias("Prix estimé")
    )

    fig = px.line(data, 
                x="kilometrage", 
                y="Prix estimé", 
                title="Prix estimé en fonction du kilométrage du véhicule",
                markers=True,
                color="type_km",
                )
    fig.update_layout(legend_title_text=None)
    fig.update_layout(xaxis=dict(tickformat='d'),
                      yaxis=dict(tickformat='d'))
    return fig


def _convert_list_float(series: pl.Series) -> pl.Series:
    """
    Convertit une série de listes en une série de valeurs flottantes.

    ## Parameters:
        series (pl.Series): Série Polars contenant des listes de valeurs.

    ## Returns:
        pl.Series: Série Polars contenant des valeurs flottantes.

    ## Example:
        >>> _convert_list_float(data['Prix estimé'])
        # Convertit une série de listes de prix en une série de valeurs flottantes.
    """
    return pl.Series(values=[val[0] for val in series])

