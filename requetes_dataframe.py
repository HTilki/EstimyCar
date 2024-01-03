"""
Module de gestion des données des véhicules.

Ce module propose une fonction permettant de filtrer les données des véhicules en fonction de différents critères
comme la marque, le modèle, l'année, le kilométrage, la boîte de vitesses, l'énergie et le prix.

"""

import duckdb
from polars import DataFrame

def get_dataframe(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int) -> DataFrame:
    """
    Filtre les données des véhicules en fonction de critères spécifiés et retourne un DataFrame.

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
        DataFrame: DataFrame Polars contenant les données des véhicules filtrées selon les critères spécifiés.

    ## Note:
        Les critères de filtrage peuvent être spécifiés individuellement ou en combinaison, selon les besoins.
    
    ## Example:
        >>> get_dataframe(['MERCEDES'], ['C220'], 2010, 2022, 0, 100000, ['Automatique'], ['Essence'], 10000, 50000)
        # Retourne un DataFrame contenant les données des véhicules de la marque MERCEDES, du modèle C220, 
        # de l'année entre 2010 et 2022, avec un kilométrage entre 0 et 100 000, une boîte de vitesses automatique,
        # fonctionnant à l'essence et avec un prix entre 10 000 et 50 000.

    """

    if marques == [] and modeles == []:
        return duckdb.sql(
            f"""
            SELECT CONCAT(
            marque, ' ', modele, ' ',
            CASE WHEN generation = 'NA' THEN '' ELSE generation END,
            ' ', finition
            ) as Véhicule, 
            cylindre, puissance, moteur, annee, boite, energie, prix, lien
            FROM 'data/database.parquet'
            WHERE annee BETWEEN {annee_min} AND {annee_max}
            AND kilometrage BETWEEN {km_min} AND {km_max}
            AND boite IN ({', '.join(f"'{b}'" for b in boite)})
            AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
            AND prix between {prix_min} AND {prix_max}
            """).pl()
    
    if marques != [] and modeles == []:
        return duckdb.sql(
            f"""
            SELECT CONCAT(
            marque, ' ', modele, ' ',
            CASE WHEN generation = 'NA' THEN '' ELSE generation END,
            ' ', finition
            ) as Véhicule, 
            cylindre, puissance, moteur, annee, boite, energie, prix, lien
            FROM 'data/database.parquet'
            WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)})
            AND annee BETWEEN {annee_min} AND {annee_max}
            AND kilometrage BETWEEN {km_min} AND {km_max}
            AND boite IN ({', '.join(f"'{b}'" for b in boite)})
            AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
            AND prix between {prix_min} AND {prix_max}
            """).pl()
    
    if marques == [] and modeles != []: 
        return duckdb.sql(
            f"""
            SELECT CONCAT(
            marque, ' ', modele, ' ',
            CASE WHEN generation = 'NA' THEN '' ELSE generation END,
            ' ', finition
            ) as Véhicule, 
            cylindre, puissance, moteur, annee, boite, energie, prix, lien
            FROM 'data/database.parquet'
            WHERE modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
            AND annee BETWEEN {annee_min} AND {annee_max}
            AND kilometrage BETWEEN {km_min} AND {km_max}
            AND boite IN ({', '.join(f"'{b}'" for b in boite)})
            AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
            AND prix between {prix_min} AND {prix_max};
            """).pl()

    if marques != [] and modeles != []: 
        return duckdb.sql(
            f"""
            SELECT CONCAT(
            marque, ' ', modele, ' ',
            CASE WHEN generation = 'NA' THEN '' ELSE generation END,
            ' ', finition
            ) as Véhicule, 
            cylindre, puissance, moteur, annee, boite, energie, prix, lien
            FROM 'data/database.parquet'
            WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)}) 
            AND modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
            AND annee BETWEEN {annee_min} AND {annee_max}
            AND kilometrage BETWEEN {km_min} AND {km_max}
            AND boite IN ({', '.join(f"'{b}'" for b in boite)})
            AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
            AND prix between {prix_min} AND {prix_max};
            """).pl()
 