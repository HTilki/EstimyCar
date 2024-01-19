"""
Module pour la manipulation des données des marques et modèles de voitures.

## Classes:
        - NomMarquesModeles: Représente une marque et sa liste de modèles.
"""


import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class NomMarquesModeles:
    marque: str
    modeles: list


def import_marques_modeles() -> list:
    """
    Importe les données des marques et leurs modèles associés disponibles à partir d'une fichier JSON et les stocke dans une liste.

    ## Returns:
            list: Liste de dataclass représentant chaque marque avec une liste de ses modèles associés.

    ## Example:
            fichier json: {
            "Marque A": ["Modèle 1", "Modèle 2"],
            "Marque B": ["Modèle 3", "Modèle 4"]
            }

            >>> [
            NomMarquesModeles(marque="Marque A", modeles=["Modèle 1", "Modèle 2"]),
            NomMarquesModeles(marque="Marque B", modeles=["Modèle 3", "Modèle 4"])
    """
    nom_marques_modeles_list = []
    with open(
        Path(".").resolve() / "json/marques_modeles.json", "r", encoding="utf-8"
    ) as json_file:
        data = json.load(json_file)
    for marque, modeles in data.items():
        nom_marques_modeles_list.append(
            NomMarquesModeles(marque=marque, modeles=modeles)
        )
    return nom_marques_modeles_list
