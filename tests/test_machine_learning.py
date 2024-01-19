"""Module de test sur le machinelearning
"""

from src.modules.machinelearning import split_data
import polars as pl
from polars.testing import assert_frame_equal


data = pl.DataFrame(
    [
        pl.Series("annee", [2023, 2018, 2021, 2024, 2021, 2022, 2007, 2023, 2024, 2021, 2021, 2024, 2023, 2023, 2023, 2021, 2021, 2018, 2022, 2023], dtype=pl.Int32),
        pl.Series("kilometrage", [13, 49583, 81900, 1150, 30740, 30836, 267086, 13171, 11, 97110, 52080, 40, 5828, 12, 9951, 62740, 26325, 144752, 39503, 16740], dtype=pl.Int64),
        pl.Series("boite", ['Automatique', 'Manuelle', 'Automatique', 'Automatique', 'Manuelle', 'Manuelle', 'Manuelle', 'Automatique', 'Manuelle', 'Manuelle', 'Manuelle', 'Manuelle', 'Manuelle', 'Manuelle', 'Manuelle', 'Manuelle', 'Automatique', 'Manuelle', 'Automatique', 'Automatique'], dtype=pl.Utf8),
        pl.Series("energie", ['Hybrides', 'Essence', 'Diesel', 'Essence', 'Essence', 'Essence', 'Essence', 'Hybrides', 'Essence', 'Diesel', 'Diesel', 'Diesel', 'Diesel', 'Diesel', 'Essence', 'Essence', 'Hybrides', 'Diesel', 'Hybrides', 'Diesel'], dtype=pl.Utf8),
        pl.Series("prix", [59490, 15970, 32160, 38230, 15670, 31230, 2470, 41420, 19600, 19770, 23630, 29360, 27290, 26650, 20890, 17140, 35080, 20150, 35980, 43380], dtype=pl.Int64),
        pl.Series("position_marché", ['Offre équitable', 'Offre équitable', 'Bonne affaire', 'Offre équitable', 'Offre équitable', 'Offre équitable', 'Très bonne affaire', 'Offre équitable', 'Bonne affaire', 'Offre équitable', 'Bonne affaire', 'Offre équitable', 'Bonne affaire', 'Bonne affaire', 'Offre équitable', 'Bonne affaire', 'Bonne affaire', 'Offre équitable', 'Offre équitable', 'Offre équitable'], dtype=pl.Utf8),
        pl.Series("garantie", [24, 0, 0, 0, 12, 12, 0, 12, 24, 12, 0, 24, 12, 0, 12, 12, 0, 0, 12, 0], dtype=pl.Int64),
        pl.Series("lien", ['https://www.lacentrale.fr/auto-occasion-annonce-69112661319.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112923461.html', 'https://www.lacentrale.fr/auto-occasion-annonce-87102793054.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112509752.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69113085500.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69111947928.html', 'https://www.lacentrale.fr/auto-occasion-annonce-87102770491.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112870907.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112450673.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112424725.html', 'https://www.lacentrale.fr/auto-occasion-annonce-66102549995.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69113145757.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112095208.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69113026731.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112886710.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112258891.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112785253.html', 'https://www.lacentrale.fr/auto-occasion-annonce-87102789728.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69113158237.html', 'https://www.lacentrale.fr/auto-occasion-annonce-69112803047.html'], dtype=pl.Utf8),
        pl.Series("marque", ['CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN', 'CITROEN'], dtype=pl.Utf8),
        pl.Series("modele", ['C5 AIRCROSS', 'C3', 'JUMPY', 'C4', 'C3', 'C4', 'C3', 'C5 AIRCROSS', 'C3', 'C3', 'JUMPY', 'BERLINGO', 'C4', 'BERLINGO', 'C3', 'C3', 'C5 AIRCROSS', 'JUMPY', 'C5 AIRCROSS', 'C5 AIRCROSS'], dtype=pl.Utf8),
        pl.Series("generation", ['phase 2', 'III', 'III FOURGON', 'III X', 'III phase 2', 'III', 'NA', 'NA', 'III phase 2', 'AIRCROSS', 'III FOURGON', 'III VAN phase 2', 'III', 'III VAN', 'III phase 2', 'III', 'NA', 'II phase 2', 'NA', 'phase 2'], dtype=pl.Utf8),
        pl.Series("cylindre", ['1.6', '1.2', '2.0', '1.2', '1.2', '1.2', '1.4', '1.6', '1.2', '1.5', '1.5', '1.5', '1.5', '1.5', '1.2', '1.2', '1.6', '2.0', '1.6', '1.5'], dtype=pl.Utf8),
        pl.Series("moteur", ['HYBRIDE', 'PURETECH', 'BLUEHDI', 'PURETECH', 'PURETECH', 'PURETECH', None, 'HYBRID', 'PURETECH', 'BLUEHDI', 'BLUEHDI', 'BLUEHDI', 'BLUEHDI', 'BLUEHDI', 'PURETECH', 'PURETECH', 'HYBRIDE', 'BLUEHDI', 'HYBRID', 'BLUEHDI'], dtype=pl.Utf8),
        pl.Series("puissance", [225, 82, 177, 131, 83, 131, 75, 225, 83, 102, 100, 100, 110, 100, 83, 110, 225, 122, 225, 131], dtype=pl.Int64),
        pl.Series("finition", ['SHINE PACK', 'FEEL BUSINESS', 'PACK DRIVER', 'SHINE PACK', 'SHINE', 'SHINE', 'PACK', 'FEEL', 'C-SERIES', 'ORIGINS', 'CLUB', None, 'SHINE', 'CLUB', 'C-SERIES', 'SHINE', 'SHINE', 'BUSINESS', 'FEEL', 'SHINE PACK'], dtype=pl.Utf8),
        pl.Series("batterie", [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], dtype=pl.Utf8),
    ]
)
    
def test_split_data():
    X, y, X_train, X_test, y_train, y_test = split_data(data, "CITROEN")
    assert_frame_equal(data[['annee', 'kilometrage', 'boite', 'energie', 'marque', 'modele', 'generation', 'cylindre', 'moteur', 'puissance', 'finition', 'batterie']], X)    
    assert_frame_equal(data[['prix']], y)
    assert len(X_train) == len(data)*0.8
    assert len(X_test) == len(data)*0.2
    assert len(y_train) == len(data)*0.8
    assert len(y_test) == len(data)*0.2
