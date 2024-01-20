"""Module de test sur le module webscraping

Ici l'annonce qui est testé correspond à ces informations : 

marque='CITROEN C3 III', 
cylindre='1.2 PURETECH 110 FEEL', 
annee='2019', 
kilometrage='10 698 km', 
boite='Automatique', 
energie='Essence', 
prix='15 990 €', 
position_marché='Bonne affaire', 
garantie='Garantie 12 mois', 
lien='https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html'
"""

from bs4 import BeautifulSoup
from pathlib import Path
from src.modules.scraping.webscraping import *
import pytest


def get_annonces_pour_test():
    """
    Récupère des annonces d'exemple à partir d'une page HTML.

    ## Returns:
        list: Liste d'objets BeautifulSoup représentant chaque annonce sur la page d'exemple.

    """
    chemin_exemple = Path(".").resolve() / "pages/exemple_annonces.html"
    page = BeautifulSoup(chemin_exemple.read_text(encoding="utf8"), features="html5lib")
    annonces = page.find_all('div', class_='searchCardContainer')
    return annonces



def test_recup_annonces():
    """
    Teste la fonction recup_annonces pour s'assurer qu'elle renvoie une liste d'objets BeautifulSoup,
    où chaque objet représente une annonce sur la page d'exemple.
    """
    annonces = get_annonces_pour_test()
    assert str(annonces[0])[:32] == '<div class="searchCardContainer"'



def test_recup_nom_vehicule():
    """
    Teste la fonction recup_nom_vehicule à partir d'une annonce.
    Vérifie que la fonction renvoie correctement le nom du véhicule pour l'annonce qui est testée.

    ## Example : 
    >>> CITROEN C3 III
    """
    annonces = get_annonces_pour_test()
    assert recup_nom_vehicule(annonces[0]) == 'CITROEN C3 III'



def test_recup_cylindre():
    """
    Teste la fonction recup_cylindre  à partir d'une annonce.
    Vérifie que la fonction renvoie correctement la cylindrée pour l'annonce qui est testée.

    ## Example :
    >>> '1.2 PURETECH 110 FEEL'
    """
    annonces = get_annonces_pour_test()
    assert recup_cylindre(annonces[0]) == '1.2 PURETECH 110 FEEL'



def test_recup_caracteristiques():
    """
    Teste la fonction recup_caracteristiques à partir d'une annonce.
    Vérifie que la fonction renvoie correctement l'année, le kilométrage, la boîte de vitesse et le type d'énergie
    pour l'annonce qui est testée.
    """
    annonces = get_annonces_pour_test()
    annee, kilometrage, boite, energie = recup_caracteristiques(annonces[0])
    assert annee == '2019'
    assert kilometrage == '10 698 km'
    assert boite == 'Automatique'
    assert energie == 'Essence'



def test_recup_prix():
    """
    Teste la fonction recup_prix à partir d'une annonce.
    Vérifie que la fonction renvoie correctement le prix pour l'annonce qui est testée.
    """
    annonces = get_annonces_pour_test()
    prix = recup_prix(annonces[0])
    assert prix == '15 990 €'



def test_recup_position_marché():
    """
    Teste la fonction recup_position_marche à partir d'une annonce.
    Vérifie que la fonction renvoie correctement la position du marché pour l'annonce qui est testée.
    """
    annonces = get_annonces_pour_test()
    position_marché = recup_position_marché(annonces[0])
    assert position_marché == 'Bonne affaire'



def test_recup_garantie():
    """
    Teste la fonction recup_garantie à partir d'une annonce.
    Vérifie que la fonction renvoie correctement la garantie pour l'annonce qui est testée.
    """
    annonces = get_annonces_pour_test()
    garantie = recup_garantie(annonces[0])
    assert garantie == 'Garantie 12 mois'



def test_recup_lien():
    """
    Teste la fonction recup_lien à partir d'une annonce.
    Vérifie que la fonction renvoie correctement le lien pour l'annonce qui est testée.
    """
    annonces = get_annonces_pour_test()
    lien = recup_href(annonces[0])
    assert lien == 'https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html'




def test_recup_data():
    """
    Teste la fonction recup_data pour la récupération des informations d'une voiture à partir d'une annonce.
    Vérifie que la fonction renvoie correctement un objet de type Voiture avec les informations correspondantes à l'annonce qui est testée.
    """
    annonces = get_annonces_pour_test()
    assert recup_data_voitures(annonces) == [voiture(marque='CITROEN C3 III', cylindre='1.2 PURETECH 110 FEEL', annee='2019', kilometrage='10 698 km', boite='Automatique', energie='Essence', prix='15 990 €', position_marché='Bonne affaire', garantie='Garantie 12 mois', lien='https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html'),
                                            voiture(marque='RENAULT CAPTUR phase 2', cylindre='1.3 TCE 130 INTENS', annee='2019', kilometrage='86 450 km', boite='Manuelle', energie='Essence', prix='13 990 €', position_marché='Bonne affaire', garantie='Garantie 12 mois', lien='https://www.lacentrale.fr/auto-occasion-annonce-69112260625.html'),
                                            voiture(marque='PEUGEOT 208 (2E GENERATION)', cylindre='1.2 PURETECH 130 ALLURE EAT8', annee='2021', kilometrage='22 935 km', boite='Automatique', energie='Essence', prix='21 990 €', position_marché='Analyse indisponible', garantie='Livraison', lien='https://www.lacentrale.fr/auto-occasion-annonce-69112617241.html'),
                                            voiture(marque='RENAULT CLIO V', cylindre='1.0 SCE 65 BUSINESS', annee='2021', kilometrage='62 317 km', boite='Manuelle', energie='Essence', prix='11 800 €', position_marché='Bonne affaire', garantie='Garantie 12 mois', lien='https://www.lacentrale.fr/auto-occasion-annonce-69113055717.html')
                                            ]
    


def test_fusionner_fichiers_json_1():
    """
    Vérifie que la fonction fusionner_fichiers_json fusionne correctement les données issues de différents fichiers JSON.
    """ 
    data_brutes = fusionner_fichiers_json(["test_data.json"])
    assert data_brutes == [{'marque': 'CITROEN C3 III',
                            'cylindre': '1.2 PURETECH 110 FEEL',
                            'annee': '2019',
                            'kilometrage': '10 698 km',
                            'boite': 'Automatique',
                            'energie': 'Essence',
                            'prix': '15 990 €',
                            'position_marché': 'Bonne affaire',
                            'garantie': 'Garantie 12 mois',
                            'lien': 'https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html'},
                            {'marque': 'RENAULT CAPTUR phase 2',
                            'cylindre': '1.3 TCE 130 INTENS',
                            'annee': '2019',
                            'kilometrage': '86 450 km',
                            'boite': 'Manuelle',
                            'energie': 'Essence',
                            'prix': '13 990 €',
                            'position_marché': 'Bonne affaire',
                            'garantie': 'Garantie 12 mois',
                            'lien': 'https://www.lacentrale.fr/auto-occasion-annonce-69112260625.html'},
                            {'marque': 'PEUGEOT 208 (2E GENERATION)',
                            'cylindre': '1.2 PURETECH 130 ALLURE EAT8',
                            'annee': '2021',
                            'kilometrage': '22 935 km',
                            'boite': 'Automatique',
                            'energie': 'Essence',
                            'prix': '21 990 €',
                            'position_marché': 'Analyse indisponible',
                            'garantie': 'Livraison',
                            'lien': 'https://www.lacentrale.fr/auto-occasion-annonce-69112617241.html'},
                            {'marque': 'RENAULT CLIO V',
                            'cylindre': '1.0 SCE 65 BUSINESS',
                            'annee': '2021',
                            'kilometrage': '62 317 km',
                            'boite': 'Manuelle',
                            'energie': 'Essence',
                            'prix': '11 800 €',
                            'position_marché': 'Bonne affaire',
                            'garantie': 'Garantie 12 mois',
                            'lien': 'https://www.lacentrale.fr/auto-occasion-annonce-69113055717.html'}]




def test_fusionner_fichiers_json_ValueError():
    """
    Vérifie que la fonction fusionner_fichiers_json génère une ValueError lorsqu'aucun fichier JSON n'est spécifié.
    """
    with pytest.raises(ValueError):
        fusionner_fichiers_json([])



def test_fusionner_fichiers_json_TypeError():
    """
    Vérifie que la fonction fusionner_fichiers_json génère une TypeError lorsqu'un argument non listé est spécifié.
    """
    with pytest.raises(TypeError):
        fusionner_fichiers_json('test_data.json')



def test_fusionner_fichiers_json_FileNotFoundError():
    """
    Vérifie que la fonction fusionner_fichiers_json génère une FileNotFoundError lorsqu'au moins l'un des 
    fichiers spécifiés n'est pas trouvé.
    """
    with pytest.raises(FileNotFoundError):
        fusionner_fichiers_json(['abcdefg.json', 'fichier_introuvable.json'])