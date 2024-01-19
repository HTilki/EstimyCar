"""Module de test sur le module datacleaning
"""

from src.modules.scraping.webscraping import fusionner_fichiers_json
from src.modules.app.import_mm import import_marques_modeles
from src.modules.datacleaning import *
from polars.testing import assert_frame_equal

def test_recup_marques_modeles_generation():
    row_ex = ("CITROEN C3 III",)
    car_ex = pl.DataFrame({
        "marque": ["CITROEN"],
        "modeles": [["C3"]]
        })
    assert recup_marque_modele_generation(row_ex, car_ex) == ('CITROEN', 'C3', 'III')


def test_get_recup_marques_modeles_generation():
    data_ex = pl.DataFrame({"marque": ["CITROEN C3 III", "RENAULT CLIO V"]})
    mrq_mod_ex = pl.DataFrame({"marque": ["CITROEN", "RENAULT"], "modeles": [["C3"], ["CLIO"]]})
    resultat = pl.DataFrame({"marque": ["CITROEN", "RENAULT"], "modele": ["C3", "CLIO"], "generation": ["III", "V"]})
    assert_frame_equal(get_marque_modele_generation(data_ex, mrq_mod_ex), resultat)

def test_get_km_prix_annee():
    data_ex = pl.DataFrame({
        "kilometrage": ["100 000 km", "75 000 km", "120 000 km"],
        "prix": ["15 000 €", "20 000 €", "12 500 €"],
        "annee": ["2015", "2018", "2012"]
        })
    resultat = pl.DataFrame(
        [
            pl.Series("kilometrage", [100000, 75000, 120000], dtype=pl.Int64),
            pl.Series("prix", [15000, 20000, 12500], dtype=pl.Int64),
            pl.Series("annee", [2015, 2018, 2012], dtype=pl.Int32),
            ]
        )
    assert_frame_equal(get_km_prix_annee(data_ex), resultat)

def test_get_garantie():
    data_ex = pl.DataFrame({"garantie": ["Livraison", "NA", "Garantie 12 mois", "3 mois", "-300 mois"]})
    resultat = pl.DataFrame({"garantie": [0, 0, 12, 3]})
    assert_frame_equal(get_garantie(data_ex), resultat)


def test_split_cylindre():
    data_ex = pl.DataFrame({"cylindre": ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", 
                            "2.0 HDI 90", "320ch 75kWh", "300ch 80kWh E-TECH"]})
    resultat = pl.DataFrame({
        'cylindre': ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", "2.0 HDI 90", "320ch 75kWh", "300ch 80kWh E-TECH"],
        'cylindre_2': ["1.6", "1.2", "1.1", None, "2.0", None, None],
        'moteur': ["BLUEHDI", "PURETECH", None, None, None, None, None],
        'puissance': ["100", "130", "60", None, None, None, None],
        'finition': ["SHINE", "FEEL PACK BUSINESS", "MIAMI", None, None, None, None],
        'puissance_2': [None, None, "60", None, None, None, None],
        'moteur_2': ["BLUEHDI", "PURETECH", None, None, "HDI", None, None],
        'puissance_3': ["100", "130", None, None, "90", None, None],
        'puissance_elec': [None, None, None, None, None, None, "300ch"],
        'batterie': [None, None, None, None, None, None, "80kWh"],
        'finition_2': [None, None, None, None, None, None, "E-TECH"],
        'puissance_elec_2': [None, None, None, None, None, "320ch", "300ch"],
        'batterie_2': [None, None, None, None, None, "75kWh", "80kWh"]
        }
    )
    assert_frame_equal(split_cylindre(data_ex), resultat)

def test_clean_cylindre():
    data_ex = pl.DataFrame({"cylindre": ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", 
                            "2.0 HDI 90", "320ch 75kWh", "300ch 80kWh E-TECH"]})
    resultat = pl.DataFrame({
        'cylindre': ["1.6", "1.2", "1.1", None, "2.0", None, None],
        'moteur': ["BLUEHDI", "PURETECH", None, None, "HDI", None, None],
        'puissance': ["100", "130", "60", None, "90", "320ch", "300ch"],
        'finition': ["SHINE", "FEEL PACK BUSINESS", "MIAMI", None, None, None, "E-TECH"],
        'batterie': [None, None, None, None, None, "75kWh", "80kWh"]
        }
    )
    assert_frame_equal(clean_cylindre(split_cylindre(data_ex)), resultat)


def test_convert_puissance():
    data_ex = pl.DataFrame({"puissance": ["320", "130ch", "60ch", None]})
    resultat = pl.DataFrame({"puissance": [320, 130, 60, None]})
    assert_frame_equal(convert_puissance(data_ex), resultat)

def test_get_cylindre():
    data_ex = pl.DataFrame({"cylindre": ["1.6 BLUEHDI 100 SHINE", "1.2 PURETECH 130 FEEL PACK BUSINESS", "1.1 60 MIAMI", "DOLLY", 
                            "2.0 HDI 90", "320ch 75kWh", "300ch 80kWh E-TECH"]})
    resultat = pl.DataFrame({
        'cylindre': ["1.6", "1.2", "1.1", None, "2.0", None, None],
        'moteur': ["BLUEHDI", "PURETECH", None, None, "HDI", None, None],
        'puissance': [100, 130, 60, None, 90, 320, 300],
        'finition': ["SHINE", "FEEL PACK BUSINESS", "MIAMI", None, None, None, "E-TECH"],
        'batterie': [None, None, None, None, None, "75kWh", "80kWh"]
        }
    )
    assert_frame_equal(get_cylindre(data_ex), resultat)

def test_filter_data():
    data_ex = pl.DataFrame({
                        "annee": [2022, 2023, 2017, 2024, 2023],
                        "kilometrage": [45000, 60000, 1500000, 55000, 80700],
                        "energie": ["essence", "erreur", "diesel", "hybride", "diesel"],
                        "puissance": [150, 120, 90, None, 100]
        })
    resultat = pl.DataFrame({
                            "annee": [2022, 2023],
                            "kilometrage": [45000, 80700],
                            "energie": ["essence", "diesel"],
                            "puissance": [150, 100]
            })
    assert_frame_equal(filter_data(data_ex), resultat)

def test_supp_doublons():
    data_ex = pl.DataFrame({
        "lien": ["https://www.lacentrale.fr/auto-occasion-annonce-69111069227.html", 
                 "https://www.lacentrale.fr/auto-occasion-annonce-87102790043.html",
                 "https://www.lacentrale.fr/auto-occasion-annonce-87102779033.html",
                 "https://www.lacentrale.fr/auto-occasion-annonce-69111069227.html"]
        })
    resultat = pl.DataFrame({
            "lien": ["https://www.lacentrale.fr/auto-occasion-annonce-69111069227.html",
                    "https://www.lacentrale.fr/auto-occasion-annonce-87102790043.html",
                    "https://www.lacentrale.fr/auto-occasion-annonce-87102779033.html"]
            })
    assert_frame_equal(supp_doublons(data_ex), resultat)

def test_supp_na():
    data_ex = pl.DataFrame({"marque": ["TOYOTA", "FORD", None, "BMW", None]})
    resultat = pl.DataFrame({"marque": ["TOYOTA", "FORD", "BMW"]})
    assert_frame_equal(supp_na(data_ex), resultat)

def test_gazoduc():
    data_brutes = pl.DataFrame(fusionner_fichiers_json(["test_data.json"]))
    nom_marques_modeles = pl.DataFrame(import_marques_modeles())
    resultat = pl.DataFrame(
    [
        pl.Series("annee", [2019, 2019, 2021, 2021], dtype=pl.Int32),
        pl.Series("kilometrage", [10698, 86450, 22935, 62317], dtype=pl.Int64),
        pl.Series("boite", ['Automatique', 'Manuelle', 'Automatique', 'Manuelle'], dtype=pl.Utf8),
        pl.Series("energie", ['Essence', 'Essence', 'Essence', 'Essence'], dtype=pl.Utf8),
        pl.Series("prix", [15990, 13990, 21990, 11800], dtype=pl.Int64),
        pl.Series("position_marché", ['Bonne affaire', 'Bonne affaire', 'Analyse indisponible', 'Bonne affaire'], dtype=pl.Utf8),
        pl.Series("garantie", [12, 12, 0, 12], dtype=pl.Int64),
        pl.Series("lien", ['https://www.lacentrale.fr/auto-occasion-annonce-69112858137.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112260625.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112617241.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69113055717.html'], dtype=pl.Utf8),
        pl.Series("marque", ['CITROEN', 'RENAULT', 'PEUGEOT', 'RENAULT'], dtype=pl.Utf8),
        pl.Series("modele", ['C3', 'CAPTUR', '208', 'CLIO'], dtype=pl.Utf8),
        pl.Series("generation", ['III', 'phase 2', '(2E GENERATION)', 'V'], dtype=pl.Utf8),
        pl.Series("cylindre", ['1.2', '1.3', '1.2', '1.0'], dtype=pl.Utf8),
        pl.Series("moteur", ['PURETECH', 'TCE', 'PURETECH', 'SCE'], dtype=pl.Utf8),
        pl.Series("puissance", [110, 130, 130, 65], dtype=pl.Int64),
        pl.Series("finition", ['FEEL', 'INTENS', 'ALLURE EAT8', 'BUSINESS'], dtype=pl.Utf8),
        pl.Series("batterie", [None, None, None, None], dtype=pl.Utf8),
    ]
    )
    assert_frame_equal(gazoduc(data_brutes, nom_marques_modeles), resultat)