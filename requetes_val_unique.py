import duckdb
from numpy import ndarray 

def get_plage_annee(user_role: str, marque: str = "", modele: str = "") -> ndarray:
    if user_role == "Acheteur":
        return duckdb.sql(
                f"""
                SELECT MIN(annee) as annee_min,
                MAX(annee) as annee_max
                FROM 'data/database.parquet'
                """).pl().to_numpy()[0]
    
    if user_role == "Vendeur":
        return duckdb.sql(
                f"""
                SELECT MIN(annee) as annee_min,
                MAX(annee) as annee_max
                FROM 'data/database.parquet'
                WHERE marque == '{marque.upper()}' 
                AND modele == '{modele.upper()}'
                """).pl().to_numpy()[0]


    
def get_unique_marque() -> list:
    marques = duckdb.sql(
        f"""
        SELECT DISTINCT(marque) as unique_mar
        FROM 'data/database.parquet'
        WHERE marque IS NOT NULL
        ORDER BY unique_mar
        """).df()
    return list(marques['unique_mar']) 

def get_unique_modele(marque: str) -> list:
    modeles = duckdb.sql(
        f"""
        SELECT DISTINCT(modele) as unique_mod
        FROM 'data/database.parquet'
        WHERE marque == '{marque.upper()}'
        AND modele IS NOT NULL
        ORDER BY unique_mod
        """).df()
    return list(modeles['unique_mod'])

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
