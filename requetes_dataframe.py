import duckdb
from polars import DataFrame

def get_dataframe(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int) -> DataFrame:

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
 