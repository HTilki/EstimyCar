"""
Module contenant des fonctions pour récupérer des statistiques sur les données des véhicules, notamment le nombre de véhicules et le prix moyen.

"""

import duckdb


def get_count_car(
    marques: list,
    modeles: list,
    annee_min: int,
    annee_max: int,
    km_min: int,
    km_max: int,
    boite: list,
    energie: list,
    prix_min: int,
    prix_max: int,
) -> int:
    """
    Récupère le nombre de véhicules correspondant aux critères spécifiés.

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
        int: Le nombre de véhicules correspondant aux critères spécifiés. En cas d'erreur, retourne 0.
    """
    try:
        if marques == [] and modeles == []:
            return (
                duckdb.sql(
                    f"""
                SELECT COUNT(*)
                FROM 'data/database.parquet'
                WHERE annee BETWEEN {annee_min} AND {annee_max}
                AND kilometrage BETWEEN {km_min} AND {km_max}
                AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                AND prix between {prix_min} AND {prix_max}
                """
                )
                .pl()
                .item()
            )
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
                AND prix between {prix_min} AND {prix_max}
                """
                )
                .pl()
                .item()
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
                AND prix between {prix_min} AND {prix_max}
                """
                )
                .pl()
                .item()
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
                AND prix between {prix_min} AND {prix_max}
                """
                )
                .pl()
                .item()
            )
    except:
        return 0
    return 0


def get_avg_price(
    marques: list | str,
    modeles: list | str,
    annee_min: int,
    annee_max: int,
    km_min: int,
    km_max: int,
    boite: list,
    energie: list,
    prix_min: int,
    prix_max: int,
    user_role: str,
    cylindre: str = "",
    puissance: int = 0,
) -> float:
    """
    Calcule et retourne le prix moyen des véhicules correspondant aux critères spécifiés.

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
        user_role (str): Le type d'utilisateur.
        cylindre (str): Par défaut "", correspond à la cylindré du véhicule.
        puissance (int): Par défaut 0, correspond à la puissance du véhicule en ch.

    ## Returns:
        float: Le prix moyen des véhicules correspondant aux critères spécifiés, arrondi à deux décimales. En cas d'erreur, retourne 0.
    """
    if user_role == "Acheteur":
        try:
            if marques == [] and modeles == []:
                prix_moyen = (
                    duckdb.sql(
                        f"""
                    SELECT ROUND(AVG(prix),2)
                    FROM 'data/database.parquet'
                    WHERE annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max}
                    """
                    )
                    .pl()
                    .item()
                )

            if marques != [] and modeles == []:
                prix_moyen = (
                    duckdb.sql(
                        f"""
                    SELECT ROUND(AVG(prix),2)
                    FROM 'data/database.parquet'
                    WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)})
                    AND annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max}
                    """
                    )
                    .pl()
                    .item()
                )

            if marques == [] and modeles != []:
                prix_moyen = (
                    duckdb.sql(
                        f"""
                    SELECT ROUND(AVG(prix),2)
                    FROM 'data/database.parquet'
                    WHERE modele IN ({', '.join(f"'{modele.upper()}'" for modele in modeles)})
                    AND annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max}
                    """
                    )
                    .pl()
                    .item()
                )

            if marques != [] and modeles != []:
                prix_moyen = (
                    duckdb.sql(
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
                    """
                    )
                    .pl()
                    .item()
                )

            if prix_moyen is None:
                prix_moyen = 0
            return prix_moyen
        except:
            return 0
    elif user_role == "Vendeur":
        try:
            prix_moyen = (
                duckdb.sql(
                    f"""
                SELECT ROUND(AVG(prix),2)
                FROM 'data/database.parquet'
                WHERE marque = '{marques}' 
                AND modele = '{modeles}'
                AND annee = {annee_max}
                AND kilometrage BETWEEN {km_max - 3000} AND {km_max + 3000}
                AND puissance BETWEEN {puissance - 10} AND {puissance + 10}
                AND boite = '{boite}'
                AND energie = '{energie}'
                AND cylindre = '{cylindre}'
                """
                )
                .pl()
                .item()
            )
            if prix_moyen is None:
                prix_moyen = 0
            return prix_moyen
        except:
            return 0
    else:
        return 0


def calcul_delta(
    marques: list,
    modeles: list,
    annee_min: int,
    annee_max: int,
    km_min: int,
    km_max: int,
    boite: list,
    energie: list,
    prix_min: int,
    prix_max: int,
):
    """
    Calcule et retourne la différence entre le nombre de véhicules correspondant aux critères spécifiés, selon la combinaison de filtres par marque et modèle.

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
        int or None: La différence entre le nombre de véhicules correspondant aux critères spécifiés, selon la combinaison de filtres par marque et modèle. En cas d'absence de critères (marques et modèles vides), retourne None.
    """
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
                """
            )
            .pl()
            .item()
            - duckdb.sql(
                f"""
                    SELECT COUNT(*)
                    FROM 'data/database.parquet'
                    WHERE annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max};
                    """
            )
            .pl()
            .item()
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
                """
            )
            .pl()
            .item()
            - duckdb.sql(
                f"""
                    SELECT COUNT(*)
                    FROM 'data/database.parquet'
                    WHERE annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max};
                    """
            )
            .pl()
            .item()
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
                """
            )
            .pl()
            .item()
            - duckdb.sql(
                f"""
                    SELECT COUNT(*)
                    FROM 'data/database.parquet'
                    WHERE marque IN ({', '.join(f"'{marque}'" for marque in marques)})
                    AND annee BETWEEN {annee_min} AND {annee_max}
                    AND kilometrage BETWEEN {km_min} AND {km_max}
                    AND boite IN ({', '.join(f"'{b}'" for b in boite)})
                    AND energie IN ({', '.join(f"'{erg}'" for erg in energie)})
                    AND prix between {prix_min} AND {prix_max};
                    """
            )
            .pl()
            .item()
        )
