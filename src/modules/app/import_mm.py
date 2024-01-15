import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class NomMarquesModeles:
        marque: str
        modeles: list
def import_marques_modeles() -> list:
        nom_marques_modeles_list = []
        with open(Path(".").resolve() / "json/marques_modeles.json", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        for marque, modeles in data.items():
                nom_marques_modeles_list.append(NomMarquesModeles(marque=marque, modeles=modeles))
        return(nom_marques_modeles_list)