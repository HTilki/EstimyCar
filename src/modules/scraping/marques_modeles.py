from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from typing import cast
from pathlib import Path


def recup_marques_modeles() -> dict:
    page_accueil = Path(".").resolve() / "pages/page_accueil.html"
    page = BeautifulSoup(page_accueil.read_text(encoding="utf8"), features="html.parser")
    div_voitures = cast(Tag, page.find("div", class_="dropdown__itemsWrapper"))
    modeles: list[str]
    marques_modeles = {}
    for marque_div in div_voitures.find_all(
        "div", class_="dropdown__itemsWrapper__brand-name"
    ):
        if isinstance(marque_div, Tag):
            nom_marque = marque_div.text.strip()
            modeles_divs = cast(
                ResultSet[Tag],
                marque_div.find_next_siblings(
                    "div", class_="dropdown__itemsWrapper__model-name"
                ),
            )
            modeles = list()
        for modele_div in modeles_divs:
            if isinstance(modele_div, Tag):
                labels = cast(
                    ResultSet[Tag],
                    modele_div.find_all(
                        "label",
                        class_="Text_Text_text Controls_Controls_label Controls_Controls_right Controls_Controls_active Text_Text_label2",
                    ),
                )
                modeles.extend(label.text.strip() for label in labels)
        marques_modeles[nom_marque] = modeles
    return marques_modeles
