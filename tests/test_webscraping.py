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
    chemin_exemple = Path(".").resolve() / "pages/exemple_annonces.html"
    page = BeautifulSoup(chemin_exemple.read_text(encoding="utf8"), features="html5lib")
    annonces = page.find_all('div', class_='searchCardContainer')
    return annonces

def test_recup_annonces():
    annonces = get_annonces_pour_test()
    assert str(annonces[0])[:32] == '<div class="searchCardContainer"'


def test_recup_nom_vehicule():
    annonces = get_annonces_pour_test()
    assert recup_nom_vehicule(annonces[0]) == 'CITROEN C3 III'


def test_recup_cylindre():
    annonces = get_annonces_pour_test()
    assert recup_cylindre(annonces[0]) == '1.2 PURETECH 110 FEEL'

def test_recup_caracteristiques():
    annonces = get_annonces_pour_test()
    annee, kilometrage, boite, energie = recup_caracteristiques(annonces[0])
    assert annee == '2019'
    assert kilometrage == '10 698 km'
    assert boite == 'Automatique'
    assert energie == 'Essence'

def test_recup_prix():
    annonces = get_annonces_pour_test()
    prix = recup_prix(annonces[0])
    assert prix == '15 990 €'

def test_recup_position_marché():
    annonces = get_annonces_pour_test()
    position_marché = recup_position_marché(annonces[0])
    assert position_marché == 'Bonne affaire'

def test_recup_garantie():
    annonces = get_annonces_pour_test()
    garantie = recup_garantie(annonces[0])
    assert garantie == 'Garantie 12 mois'

def test_recup_lien():
    annonces = get_annonces_pour_test()
    lien = recup_href(annonces[0])
    assert lien == 'https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html'



def test_recup_informations_voiture():
    annonces = get_annonces_pour_test()
    assert recup_informations_voiture(annonces[0]) == voiture(marque='CITROEN C3 III', 
                                                              cylindre='1.2 PURETECH 110 FEEL', 
                                                              annee='2019', 
                                                              kilometrage='10 698 km',
                                                              boite='Automatique', 
                                                              energie='Essence', 
                                                              prix='15 990 €', 
                                                              position_marché='Bonne affaire', 
                                                              garantie='Garantie 12 mois', 
                                                              lien='https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html')
    

def test_recup_data():
    annonces = get_annonces_pour_test()
    assert recup_data_voitures(annonces) == [voiture(marque='CITROEN C3 III', cylindre='1.2 PURETECH 110 FEEL', annee='2019', kilometrage='10 698 km', boite='Automatique', energie='Essence', prix='15 990 €', position_marché='Bonne affaire', garantie='Garantie 12 mois', lien='https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html'),
                                             voiture(marque='RENAULT CAPTUR phase 2', cylindre='1.3 TCE 130 INTENS', annee='2019', kilometrage='86 450 km', boite='Manuelle', energie='Essence', prix='13 990 €', position_marché='Bonne affaire', garantie='Garantie 12 mois', lien='https://www.lacentrale.fr/auto-occasion-annonce-69112260625.html'),
                                             voiture(marque='PEUGEOT 208 (2E GENERATION)', cylindre='1.2 PURETECH 130 ALLURE EAT8', annee='2021', kilometrage='22 935 km', boite='Automatique', energie='Essence', prix='21 990 €', position_marché='Analyse indisponible', garantie='Livraison', lien='https://www.lacentrale.fr/auto-occasion-annonce-69112617241.html'),
                                             voiture(marque='RENAULT CLIO V', cylindre='1.0 SCE 65 BUSINESS', annee='2021', kilometrage='62 317 km', boite='Manuelle', energie='Essence', prix='11 800 €', position_marché='Bonne affaire', garantie='Garantie 12 mois', lien='https://www.lacentrale.fr/auto-occasion-annonce-69113055717.html')
                                            ]
    
def test_fusionner_fichiers_json_1():
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
    with pytest.raises(ValueError):
        fusionner_fichiers_json([])

def test_fusionner_fichiers_json_TypeError():
    with pytest.raises(TypeError):
        fusionner_fichiers_json('test_data.json')

def test_fusionner_fichiers_json_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        fusionner_fichiers_json(['abcdefg.json', 'fichier_introuvable.json'])