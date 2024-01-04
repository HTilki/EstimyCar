import polars as pl
import re

def recup_marque_modele_generation(row: tuple, nom_marques_modeles: pl.DataFrame) -> tuple:
    """
    Récupère les informations sur la marque, le modèle et la génération d'un véhicule.

    ## Parameters:
        row (tuple): Tuple contenant une chaîne de caractères représentant les informations du véhicule.
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules. 

    ## Returns:
        - Un tuple contenant la marque, le modèle et la génération du véhicule s'ils sont identifiés.
        - Sinon retourne None si aucune correspondance n'est trouvée.

    ## Example:
        >>> row_ex = ("CITROEN C3 2010",)
        >>> car_ex = pl.DataFrame({
        ...     "marque": ["CITROEN"],
        ...     "modeles": [["C3"]]
        ... })
        >>> recup_marque_modele_generation(row_ex, car_ex)
        ('CITROEN', 'C3', '2010')
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
    Extrait les informations sur la marque, le modèle et la génération à partir des données fournies.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules. 


    ## Returns:
        pl.DataFrame: DataFrame Polars contenant les informations sur la marque, le modèle et la génération extraites des données fournies.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ... "marque": ["CITROEN C3 2010", "MERCEDES 280 SL 1971"],
        ...  #...
        })

        >>> mrq_mod_ex = pl.DataFrame({
        ... "marque": ["CITROEN", "MERCEDES"],
        ... "modeles": [["C3"], ["280"]]
        })

        >>> get_marque_modele_generation(data_ex, mrq_mod_ex)
        | marque    | modele | generation |
        |-----------|--------|------------|
        | CITROEN   | C3     | 2010       |
        | MERCEDES  | 280    | SL 1971    |

    """
    data = data.with_columns(
        data.select(pl.col('marque')).map_rows(lambda row: recup_marque_modele_generation(row, nom_marques_modeles))
    ).drop("marque").rename({"column_0": "marque", "column_1": "modele", "column_2": "generation"})
    return data


def get_km_prix_annee(data: pl.DataFrame) -> pl.DataFrame:
    """
    Traite les données des colonnes "kilométrage", "prix" et "année" dans le DataFrame fourni.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars traité, avec les colonnes '"kilométrage", "prix" et "année" converties dans le bon format.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "kilometrage": ["100 000 km", "75 000 km", "120 000 km"],
        ...     "prix": ["15 000 €", "20 000 €", "12 500 €"],
        ...     "annee": ["2015", "2018", "2012"]
        ... })

        >>> get_km_prix_annee(data_ex)
        | kilometrage | prix | annee |
        |-------------|------|-------|
        | 100000      | 15000| 2015  |
        | 75000       | 20000| 2018  |
        | 120000      | 12500| 2012  |

    """
    data = data.with_columns(
        pl.col("kilometrage").str.replace_all(" ", "").str.replace("km", "").cast(pl.Int64),
        pl.col("prix").str.replace("€", "").str.replace_all(" ", "").cast(pl.Int64),
        pl.col("annee").cast(pl.Int32)
    )
    return data


def get_garantie(data : pl .DataFrame) -> pl.DataFrame :
    """
    Traite les données de la colonne "garantie" dans le DataFrame fourni.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars traité, avec la colonne "garantie" nettoyer et convertie dans le bon format.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "garantie": ["Livraison", "NA", "Garantie 12 mois", "3 mois", "-300 mois"]
        ...     # ... 
        ... })

        >>> get_garantie(data_ex)
        |garantie |
        |---------|
        | 0       |
        | 0       |
        | 12      |
        | 3       |

    """
    data = data.with_columns(
        pl.col("garantie").str.replace("Livraison", "0").str.replace("NA", "0").str.replace("Garantie", "").str.replace("mois", "").str.replace_all(" ", "")
    ).filter(~(pl.col("garantie").str.contains(r"-\d{3}"))).with_columns(
        pl.col("garantie").str.replace("-", "").cast(pl.Int64)
    )
    return data


def split_cylindre(data: pl.DataFrame) -> pl.DataFrame:
    """
    Divise et extrait les informations de cylindre, puissance, moteur, batterie et finition à partir de la colonne "cylindre".

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars traité, avec les nouvelles colonnes "cylindre_2"", "moteur", "puissance", "finition", 
        "puissance_2", "puissance_elec", "batterie", "finition_2" extraites de la colonne "cylindre".

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "cylindre": ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", 
                            "2.0 HDI 90", "320ch 75kWh"]
        ...     # ...
        ... })

        >>> split_cylindre(data_ex)
        | cylindre                             | cylindre_2 | moteur    | puissance | finition            | puissance_2 | puissance_elec | batterie | finition_2 | puissance_elec_2 | batterie_2 |
        |--------------------------------------|------------|-----------|-----------|---------------------|-------------|----------------|----------|-------------|------------------|------------|
        | "1.6 BLUEHDI 100 SHINE"              | "1.6"      | "BLUEHDI" | "100"     | "SHINE"             | null        | null           | null     | null        | null             | null       |
        | "1.2 PURETECH 130 FEEL PACK BUSINESS"| "1.2"      | "PURETECH"| "130"     | "FEEL PACK BUSINESS"| null        | null           | null     | null        | null             | null       |
        | "1.1 60 MIAMI"                       | "1.1"      | null      | "60"      | "MIAMI"             | "60"        | null           | null     | null        | null             | null       |
        | "DOLLY"                              | null       | null      | null      | null                | null        | null           | null     | null        | null             | null       |
        | "2.0 HDI 90"                         | "2.0"      | null      | null      | null                | null        | null           | null     | null        | null             | null       |
        | "320ch 75kWh"                        | null       | null      | null      | null                | null        | null           | null     | null        | "320ch"          | "75kWh"    |

        

    """
    MOTIF1 = r'(?P<cylindre>\d+\.\d+)\s+(?:(?P<moteur>[\w-]+)\s+)?(?P<puissance>\d+)\s+(?P<finition>\w+.*)'
    MOTIF2 = r'(?P<cylindre>\d+\.\d+)\s+(?P<puissance>\d+)'
    MOTIF3 = r'(?P<cylindre>\d+\.\d+)\s+(?P<moteur>[\w-]+)\s+?(?P<puissance>\d+)'
    MOTIF_ELEC = r'(?P<puissance>\d+ch)\s+(?P<batterie>\d+kWh)\s+(?P<finition>\w+.*)'
    MOTIF_ELEC2 = r'(?P<puissance>\d+ch)\s+(?P<batterie>\d+kWh+)'
    MOTIF_CYLINDRE = r'(?P<cylindre>\d+\.\d+)'
    data = data.with_columns(
        pl.col('cylindre').str.extract(MOTIF_CYLINDRE, 1).alias("cylindre_2"),
        pl.col('cylindre').str.extract(MOTIF1, 2).alias("moteur"),
        pl.col('cylindre').str.extract(MOTIF1, 3).alias("puissance"),
        pl.col('cylindre').str.extract(MOTIF1, 4).alias("finition"),
        pl.col('cylindre').str.extract(MOTIF2, 2).alias("puissance_2"),
        pl.col('cylindre').str.extract(MOTIF3, 2).alias("moteur_2"),
        pl.col('cylindre').str.extract(MOTIF3, 3).alias("puissance_3"),
        pl.col('cylindre').str.extract(MOTIF_ELEC, 1).alias("puissance_elec"),
        pl.col('cylindre').str.extract(MOTIF_ELEC, 2).alias("batterie"),
        pl.col('cylindre').str.extract(MOTIF_ELEC, 3).alias("finition_2"),
        pl.col('cylindre').str.extract(MOTIF_ELEC2, 1).alias("puissance_elec_2"),
        pl.col('cylindre').str.extract(MOTIF_ELEC2, 2).alias("batterie_2")
    )
    return data


def clean_cylindre(data: pl.DataFrame) -> pl.DataFrame:
    """
    Nettoie et organise les données de puissance et de finition à partir de colonnes spécifiques.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars avec les colonnes "puissance" et "finition" restructurées et renommées.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "cylindre": ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", 
                            "2.0 HDI 90", "320ch 75kWh"]
        ...     # ...
        ... })

        >>> clean_cylindre(split_cylindre(data_ex))
        | cylindre | moteur    | puissance | finition            | batterie |
        |----------|-----------|-----------|---------------------|----------|
        | "1.6"    | "BLUEHDI" | "100"     | "SHINE"             | null     |
        | "1.2"    | "PURETECH"| "130"     | "FEEL PACK BUSINESS"| null     |
        | "1.1"    | null      | "60"      | "MIAMI"             | null     |
        | null     | null      | null      | null                | null     |
        | "2.0"    | null      | null      | null                | null     |
        | null     | null      | "320ch"   | null                | "75kWh"  |

    """
    data = data.with_columns(
    pl.when(pl.col("puissance").is_null())
    .then(pl.col("puissance_2"))
    .otherwise(pl.col("puissance"))
    .alias("puissance")
    ).with_columns(
    pl.when(pl.col("puissance").is_null())
    .then(pl.col("puissance_3"))
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
    ).with_columns(
    pl.when(pl.col("moteur").is_null())
    .then(pl.col("moteur_2"))
    .otherwise(pl.col("moteur"))
    .alias("moteur")
    ).drop(['cylindre', 'moteur_2', 'puissance_2', 'puissance_3', 'finition_2', 'puissance_elec', 'puissance_elec_2', 'batterie_2']
           ).rename({'cylindre_2': "cylindre"})
    return data

def convert_puissance(data: pl.DataFrame) -> pl.DataFrame:
    """
    Modifie le format des données de la colonne "puissance" du DataFrame donné.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars avec la colonne "puissance" convertie au format spécifié.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "puissance": ["320", "130ch", "60ch", None]
        ...     # ... 
        ... })

        >>> convert_puissance(data_ex)
        | puissance |
        |-----------|
        | 320       |
        | 130       |
        | 60        |
        | null      |

    """
    data = data.with_columns(
        pl.col("puissance").str.replace_all("ch", "").cast(pl.Int64),
    )
    return data

def get_cylindre(data: pl.DataFrame) -> pl.DataFrame:
    """
    Effectue une série de traitements sur les colonnes du DataFrame pour obtenir des données formatées sur les cylindres des véhicules.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame:  DataFrame Polars avec les colonnes formatées sur les cylindres et la puissance.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "cylindre": ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", 
                            "2.0 HDI 90", "320ch 75kWh"]
        ...     # ...
        ... })

        >>> get_cylindre(data_ex)
        | cylindre | moteur    | puissance | finition            | batterie |
        |----------|-----------|-----------|---------------------|----------|
        | "1.6"    | "BLUEHDI" |  100      | "SHINE"             | null     |
        | "1.2"    | "PURETECH"|  130      | "FEEL PACK BUSINESS"| null     |
        | "1.1"    | null      |  60       | "MIAMI"             | null     |
        | null     | null      | null      | null                | null     |
        | "2.0"    | null      | null      | null                | null     |
        | null     | null      |  320      | null                | "75kWh"  |

    """
    data = (data.pipe(split_cylindre)
            .pipe(clean_cylindre)
            .pipe(convert_puissance)
            )
    return data


def filter_data(data: pl.DataFrame) -> pl.DataFrame:
    """
    Filtre les données en supprimant les lignes ayant une année égale à 2024 et un kilométrage supérieur à 50000, 
    les lignes ayant une énergie marquée comme "erreur", ainsi que les lignes n'ayant pas de puissance.


    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars filtré selon les spécifications indiquées.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "annee": [2022, 2023, 2017, 2024, 2023],
        ...     "kilometrage": [45000, 60000, 1500000, 55000, 80700],
        ...     "energie": ["essence", "erreur", "diesel", "hybride", "diesel"],
        ...     "puissance": [150, 120, 90, None, 100]
        })

        >>> filter_data(data_ex)
        | annee | kilometrage | energie  | puissance |
        |-------|-------------|----------|-----------|
        | 2022  | 45000       | "essence"| 150       |
        | 2017  | 1500000     | "diesel" | 90        |
        | 2023  | 80700       | "diesel" | 100       |

    """
    data = data.filter(
        ~((pl.col("annee") == 2024) & (pl.col("kilometrage") > 50000))
        ).filter(
            pl.col("energie") != "erreur"
            ).filter(pl.col("puissance").is_not_null())
    return data

def supp_doublons(data: pl.DataFrame) -> pl.DataFrame:
    """
    Supprime les doublons en se basant sur la colonne "lien".

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars avec les doublons supprimés.

    ## Example: 
        >>> data_ex = pl.DataFrame({
        ...     "lien": ["https://www.lacentrale.fr/auto-occasion-annonce-69111069227.html", 
        ...             "https://www.lacentrale.fr/auto-occasion-annonce-87102790043.html",
        ...             "https://www.lacentrale.fr/auto-occasion-annonce-87102779033.html",
        ...             "https://www.lacentrale.fr/auto-occasion-annonce-69111069227.html"]
        })

        >>> supp_doublons(data_ex)
        | lien                                                              |
        |-------------------------------------------------------------------|
        | https://www.lacentrale.fr/auto-occasion-annonce-69111069227.html  |
        | https://www.lacentrale.fr/auto-occasion-annonce-87102790043.html  |
        | https://www.lacentrale.fr/auto-occasion-annonce-87102779033.html  |
    """
    data = data.unique(subset=["lien"])
    return data


def supp_na(data: pl.DataFrame) -> pl.DataFrame:
    """
    Supprime les lignes du DataFrame  où la valeur de la colonne "marque"" est manquante (null).

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.

    ## Returns:
        pl.DataFrame: DataFrame Polars avec les lignes contenant des valeurs manquantes dans la colonne "marque" supprimées.

    ## Example:
        >>> data_ex = pl.DataFrame({
        ...     "marque": ["Toyota", "Ford", None, "BMW", None]
        ...     # ...
        ... })

        >>> supp_na(data_ex)
        | marque |
        |--------|
        | Toyota |
        | Ford   |
        | BMW    |
    """
    data = data.drop_nulls(subset="marque")
    return data


def gazoduc(data: pl.DataFrame, nom_marques_modeles: pl.DataFrame) -> pl.DataFrame:
    """
    Applique un pipeline de traitement de données sur le DataFrame donné en utilisant plusieurs fonctions :

    1. Obtention de la marque, du modèle et de la génération des véhicules.
    2. Conversion et extraction des informations sur le kilométrage, le prix et l'année.
    3. Traitement des données de garantie.
    4. Extraction et mise en forme des données sur les cylindres.
    5. Filtrage des données basé sur des critères spécifiques.
    6. Suppression des doublons.
    7. Suppression des lignes ayant des valeurs manquantes dans la colonne 'marque'.

    ## Parameters:
        data (pl.DataFrame): DataFrame Polars contenant les caractéristiques des véhicules à traiter.
        nom_marques_modeles (pl.DataFrame): DataFrame Polars contenant la liste des marques et  les modèles associés des véhicules. 

    ## Returns:
        pl.DataFrame: DataFrame Polars suite au traitement de pipeline, après avoir appliqué plusieurs étapes de transformation et de nettoyage.
    """
    data = (data.pipe(get_marque_modele_generation, nom_marques_modeles)
            .pipe(get_km_prix_annee)
            .pipe(get_garantie)
            .pipe(get_cylindre)
            .pipe(filter_data)
            .pipe(supp_doublons)
            .pipe(supp_na)
    )
    return data