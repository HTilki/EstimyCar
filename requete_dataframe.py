import duckdb
from polars import DataFrame


def get_count_car(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int) -> int:
    try:           
        if marques == [] and modeles == []:
            return duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()
        if marques != [] and modeles == []:
            return duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()
        if marques == [] and modeles != []: 
            return duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()
        if marques != [] and modeles != []: 
            return duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)}) 
                AND modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()
    except: 
        return "0"

def get_avg_price(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int) -> str:
    
    try:
        if marques == [] and modeles == []:
            prix_moyen =  duckdb.sql(
                f"""
                SELECT ROUND(AVG(prix),2)
                FROM 'data/database.parquet'
                WHERE annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()
        
        if marques != [] and modeles == []:
            prix_moyen = duckdb.sql(
                f"""
                SELECT ROUND(AVG(prix),2)
                FROM 'data/database.parquet'
                WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()

        if marques == [] and modeles != []: 
            prix_moyen = duckdb.sql(
                f"""
                SELECT ROUND(AVG(prix),2)
                FROM 'data/database.parquet'
                WHERE modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()

        if marques != [] and modeles != []: 
            prix_moyen = duckdb.sql(
                f"""
                SELECT ROUND(AVG(prix),2)
                FROM 'data/database.parquet'
                WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)}) 
                AND modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """).pl().item()

        if prix_moyen is None:
            prix_moyen = "0€"
        else:
            prix_moyen = str(prix_moyen) + '€'
        return prix_moyen
    except: 
        return "0 €"

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
    
def get_plage_annee():
    return duckdb.sql(
            f"""
            SELECT MIN(annee) as annee_min,
            MAX(annee) as annee_max
            FROM 'data/database.parquet'
            """).pl().to_numpy()[0]


def calcul_delta(marques: list, modeles: list, annee_min: int, annee_max: int, km_min: int, km_max: int, boite: list, energie: list, prix_min: int, prix_max: int):
    
    if marques == [] and modeles == []:
        return None
    
    if marques != [] and modeles == []:
        return (
            duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)}) 
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max};
                """).pl().item()
                -
                duckdb.sql(
                    f"""
                    SELECT COUNT(*)
                    FROM 'data/database.parquet'
                    WHERE annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max};
                    """).pl().item()
                    )
    
    if marques == [] and modeles != []:
        return (
            duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max};
                """).pl().item()
                -
                duckdb.sql(
                    f"""
                    SELECT COUNT(*)
                    FROM 'data/database.parquet'
                    WHERE annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max};
                    """).pl().item()
                    )

    if marques != [] and modeles != []:
        return (
            duckdb.sql(
                f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)}) 
                AND modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                AND annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max};
                """).pl().item()
                -
                duckdb.sql(
                    f"""
                    SELECT COUNT(*)
                    FROM 'data/database.parquet'
                    WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)})
                    AND annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max};
                    """).pl().item()
                    )

def get_unique_generation(marque: str, modele: str) -> list:
    generations = duckdb.sql(
        f"""
        SELECT DISTINCT(generation) as unique_gen
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND generation IS NOT NULL
        ORDER BY unique_gen
        """).df()
    return list(generations['unique_gen'])    

def get_unique_moteur(marque: str, modele: str) -> list:
    moteurs = duckdb.sql(
        f"""
        SELECT DISTINCT(moteur) as unique_mot
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND moteur IS NOT NULL
        ORDER BY unique_mot 
        """).df()
    return list(moteurs['unique_mot'])

def get_unique_cylindre(marque: str, modele: str) -> list:
    cylindres = duckdb.sql(
        f"""
        SELECT DISTINCT(cylindre) as unique_cyl
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND cylindre IS NOT NULL
        ORDER BY unique_cyl
        """).df()
    return list(cylindres['unique_cyl'])

def get_unique_finition(marque: str, modele: str) -> list:
    finitions = duckdb.sql(
        f"""
        SELECT DISTINCT(finition) as unique_fin
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}' 
        AND modele == '{modele.upper()}'
        AND finition IS NOT NULL
        ORDER BY unique_fin
        """).df()
    return list(finitions['unique_fin'])

def get_unique_batterie() -> list:
    batteries = duckdb.sql(
        f"""
        SELECT DISTINCT(batterie) as unique_bat
        FROM 'data/database.parquet'
        WHERE batterie IS NOT NULL
        ORDER BY unique_bat
        """).df()
    return list(batteries['unique_bat'])
