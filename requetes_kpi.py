import duckdb

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