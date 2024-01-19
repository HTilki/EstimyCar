"""
Module de prédiction de prix de véhicules.

Ce module contient des fonctions pour l'entraînement de modèles de régression, la prédiction des prix de véhicules,
et la gestion des modèles sauvegardés.

"""

import polars as pl
import pandas as pd
import numpy as np
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from joblib import dump
import duckdb
from src.modules.app.import_mm import import_marques_modeles

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
    return  ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

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
        - 'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        - 'weights': ['uniform', 'distance']
    - 'RandomForest':
        - 'n_estimators': [500, 800]
        - 'max_depth': [10, 15]
        - 'min_samples_split': [5, 10, 15]
        - 'min_samples_leaf': [2]

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
            'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'weights': ['uniform', 'distance']
        },
        'RandomForest': {
            'n_estimators': [500, 800],
            'max_depth': [10, 15],
            'min_samples_split': [5, 10, 15],
            'min_samples_leaf': [2]
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


def get_all_models() -> None:
    """
    Entraîne, évalue et exporte le meilleur modèle pour chaque marque parmis les 40 marques avec le plus d'observations.

    ## Returns:
        None

    ## Example:
        >>> get_all_models()
        # Les résultats sont exportés pour chaque modèle.

    ## Notes:
        Les résultats de la recherche sur grille et les informations des meilleurs modèles sont exportés
        dans le répertoire 'cv_results' avec les noms '{marque}_{model_name}_results.json'.
        
        Les meilleurs modèles et preprocesseur associés sont exporté dans le dossier src/models avec les noms 
        '{marque}_best_model.joblib' et '{marque}_preprocessor.joblib' respectivement.
    """
    warnings.filterwarnings("ignore")
    nom_marques_modeles = pl.DataFrame(import_marques_modeles()).head(40)
    data = duckdb.sql(
        """
        SELECT *
        FROM 'data/database.parquet'
        """).pl()
    for marque in nom_marques_modeles['marque'].to_numpy():
        preprocess_train_and_evaluate_model(data, marque)


def cv_result_into_df(modele: str, marques_array: np.ndarray) -> pl.DataFrame:
    """
    Convertit les résultats de la validation croisée en polars DataFrame pour un modèle et des marques spécifiques.

    ## Parameters:
        modele (str): Le nom du modèle pour lequel récupérer les résultats de la validation croisée.
        marques_array (np.ndarray): Un tableau NumPy contenant les noms des marques.

    ## Returns:
        pl.DataFrame: Un DataFrame contenant les résultats de la validation croisée pour le modèle et les marques spécifiés.
    """

    for marque in marques_array:
        if marque[0] == marques_array[0,0]:
            cv_results = duckdb.sql(
                f"""
                SELECT '{marque[0]}' as marque,
                mean_test_score,
                '{modele}' as modele,
                params
                FROM 'cv_results/{marque[0]}_{modele}_results.json'
                WHERE rank_test_score = 1
                """).pl().unnest('params')
        else :
            cv_results_2 = duckdb.sql(
                f"""
                SELECT '{marque[0]}' as marque,
                mean_test_score,
                '{modele}' as modele,
                params
                FROM 'cv_results/{marque[0]}_{modele}_results.json'

                WHERE rank_test_score = 1
                """).pl().unnest('params')
            cv_results = pl.concat([cv_results, cv_results_2], rechunk=True)
    return cv_results
