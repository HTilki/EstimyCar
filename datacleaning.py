import polars as pl
import re

def recup_marque_modele_generation(row: tuple, nom_marques_modeles: pl.DataFrame) -> tuple:
    """
    Récupère les informations sur la marque, le modèle et la génération d'un véhicule.

    Args:
        row (tuple): Tuple contenant une chaîne de caractères représentant les informations du véhicule.
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et les modèles associés des véhicules.

    Returns:
        - Un tuple contenant la marque, le modèle et la génération du véhicule s'ils sont identifiés.
        - Retourne None si aucune correspondance n'est trouvée.

    Example:
        >>> row_example = ("MERCEDES 280 SL 1971",)
        >>> nom_marques_modeles_example = pl.DataFrame({
        ...    "marque": ["MERCEDES"],
        ...    "modeles": [["280 SL"]]
        ... })
        >>> recup_marque_modele_generation(row_example, nom_marques_modeles_example)
        ('MERCEDES', '280 SL', '1971')
    """
    for marque in nom_marques_modeles["marque"]:
        # On teste la presence de la marque dans la chaine de caractère
        if marque + ' ' in row[0]:
            modeles = nom_marques_modeles.filter(nom_marques_modeles['marque'] == marque)['modeles'][0]
            # Si la marque est présente on teste la présence d'un des modèles de la marques
            for modele in modeles:
                if modele.upper() + ' ' in row[0]:
                    # Si il y a le modèle + d'autre caractere après ceux ci sont attribué à la génération du véhicule
                    generation = row[0].replace(marque + ' ' + modele.upper() + ' ', '')
                    return (marque, modele.upper(), generation)
                elif modele.upper() in row[0]:
                    # cas où il n'y a que la marque et le modèle 
                    pattern = f"{marque} {modele.upper()}(.*$)"
                    match = re.match(pattern, row[0])
                    if match:
                        generation = "NA"
                        return (marque, modele.upper(), generation)
                    
def get_marque_modele_generation(data: pl.DataFrame, nom_marques_modeles: pl.DataFrame) -> pl.DataFrame:
    """
    Récupère les informations de marque, modèle et génération pour chaque véhicule dans le DataFrame.

    Args:
        data (pl.DataFrame): DataFrame Polars contenant la colonne 'marque' avec les informations sur les véhicules.
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et les modèles associés des véhicules.

    Returns:
        Un nouveau DataFrame avec les colonnes 'marque', 'modele' et 'generation' ajoutées, et la colonne 'marque' d'origine supprimée.

    Example:
        >>> data_example = pl.DataFrame({
        ...     "marque": ["CITROEN C3 2010", "MERCEDES 280 SL 1971"],
        ...     # ... (autres colonnes)
        ... })
        >>> nom_marques_modeles_example = pl.DataFrame({
        ...     "marque": ["CITROEN", "MERCEDES"],
        ...     "modeles": [["C3"], ["280 SL"]]
        ... })
        >>> get_marque_modele_generation(data_example, nom_marques_modeles_example)
        shape: (2, 2)
        ┌─────────┬────────────┬────────────┐
        │ marque  │ modele     │ generation │
        │ ---     │ ---        │ ---        │
        ├─────────┼────────────┼────────────┤
        │ CITROEN │ C3         │ 2010       │
        │ MERCEDES│ 280 SL     │ 1971       │
        └─────────┴────────────┴────────────┘
    """
    data = data.with_columns(
        data.select(pl.col('marque')).map_rows(lambda row: recup_marque_modele_generation(row, nom_marques_modeles))
    ).drop("marque").rename({"column_0": "marque", "column_1": "modele", "column_2": "generation"})
    return data


def get_km_prix_annee(data: pl.DataFrame) -> pl.DataFrame:
    data = data.with_columns(
        pl.col("kilometrage").str.replace_all(" ", "").str.replace("km", "").cast(pl.Int64),
        pl.col("prix").str.replace("€", "").str.replace_all(" ", "").cast(pl.Int64),
        pl.col("annee").cast(pl.Int32)
    )
    return data


def get_garantie(data : pl .DataFrame) -> pl.DataFrame :
    data = data.with_columns(
        pl.col("garantie").str.replace("Livraison", "0").str.replace("NA", "0").str.replace("Garantie", "").str.replace("mois", "").str.replace_all(" ", "")
    ).filter(~(pl.col("garantie").str.contains(r"-\d{3}"))).with_columns(
        pl.col("garantie").str.replace("-", "").cast(pl.Int64)
    )
    return data


def split_cylindre(data: pl.DataFrame) -> pl.DataFrame:
    MOTIF1 = r'(?P<cylindre>\d+\.\d+)\s+(?:(?P<moteur>[\w-]+)\s+)?(?P<puissance>\d+)\s+(?P<finition>\w+.*)'
    MOTIF2 = r'(?P<cylindre>\d+\.\d+)\s+(?P<puissance>\d+)'
    MOTIF_ELEC = r'(?P<puissance>\d+ch)\s+(?P<batterie>\d+kWh)\s+(?P<finition>\w+.*)'
    MOTIF_ELEC2 = r'(?P<puissance>\d+ch)\s+(?P<batterie>\d+kWh+)'
    MOTIF_CYLINDRE = r'(?P<cylindre>\d+\.\d+)'
    data = data.with_columns(
        pl.col('cylindre').str.extract(MOTIF_CYLINDRE, 1).alias("cylindre_2"),
        pl.col('cylindre').str.extract(MOTIF1, 2).alias("moteur"),
        pl.col('cylindre').str.extract(MOTIF1, 3).alias("puissance"),
        pl.col('cylindre').str.extract(MOTIF1, 4).alias("finition"),
        pl.col('cylindre').str.extract(MOTIF2, 2).alias("puissance_2"),
        pl.col('cylindre').str.extract(MOTIF_ELEC, 1).alias("puissance_elec"),
        pl.col('cylindre').str.extract(MOTIF_ELEC, 2).alias("batterie"),
        pl.col('cylindre').str.extract(MOTIF_ELEC, 3).alias("finition_2"),
        pl.col('cylindre').str.extract(MOTIF_ELEC2, 1).alias("puissance_elec_2"),
        pl.col('cylindre').str.extract(MOTIF_ELEC2, 2).alias("batterie_2")
    )
    return data


def clean_cylindre(data: pl.DataFrame) -> pl.DataFrame:
    data = data.with_columns(
    pl.when(pl.col("puissance").is_null())
    .then(pl.col("puissance_2"))
    .otherwise(pl.col("puissance"))
    .alias("puissance")
    ).with_columns(
    pl.when(pl.col("puissance").is_null())
    .then(pl.col("puissance_elec"))
    .otherwise(pl.col("puissance"))
    .alias("puissance")
    ).with_columns(
    pl.when(pl.col("puissance").is_null())
    .then(pl.col("puissance_elec_2"))
    .otherwise(pl.col("puissance"))
    .alias("puissance")
    ).with_columns(
    pl.when(pl.col("finition").is_null())
    .then(pl.col("finition_2"))
    .otherwise(pl.col("finition"))
    .alias("finition")
    ).drop(['cylindre', 'puissance_2', 'finition_2', 'puissance_elec']
    ).with_columns(
    pl.when(pl.col("batterie").is_null())
    .then(pl.col("batterie_2"))
    .otherwise(pl.col("batterie"))
    .alias("batterie")
    ).drop(['cylindre', 'puissance_2', 'finition_2', 'puissance_elec', 'puissance_elec_2', 'batterie_2']
           ).rename({'cylindre_2': "cylindre"})
    return data

def convert_puissance(data: pl.DataFrame) -> pl.DataFrame:
    data = data.with_columns(
        pl.col("puissance").str.replace_all("ch", "").cast(pl.Int64),
    )
    return data

def get_cylindre(data: pl.DataFrame) -> pl.DataFrame:
    data = (data.pipe(split_cylindre)
            .pipe(clean_cylindre)
            .pipe(convert_puissance)
            )
    return data


def filter_data(data: pl.DataFrame) -> pl.DataFrame:
    data = data.filter(
        ~((pl.col("annee") == 2024) & (pl.col("kilometrage") > 50000))
        ).filter(
            pl.col("energie") != "erreur"
            ).filter(pl.col("puissance").is_not_null())
    return data

def supp_doublons(data: pl.DataFrame) -> pl.DataFrame:
    data = data.unique(subset=["lien"])
    return data


def supp_na(data: pl.DataFrame) -> pl.DataFrame:
    data = data.drop_nulls(subset="marque")
    return data


def gazoduc(data: pl.DataFrame, nom_marques_modeles: pl.DataFrame) -> pl.DataFrame:
    data = (data.pipe(get_marque_modele_generation, nom_marques_modeles)
            .pipe(get_km_prix_annee)
            .pipe(get_garantie)
            .pipe(get_cylindre)
            .pipe(filter_data)
            .pipe(supp_doublons)
            .pipe(supp_na)
    )
    return data