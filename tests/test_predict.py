"""Module de test sur le module predict
"""

from src.modules.app.predict import  predict_prix
import polars as pl
import numpy as np

def test_predict_prix_rf():
    data_to_predict = pl.DataFrame(
        [
            pl.Series("annee", [2015], dtype=pl.Int32),
            pl.Series("kilometrage", [116671], dtype=pl.Int64),
            pl.Series("boite", ['Manuelle'], dtype=pl.Utf8),
            pl.Series("energie", ['Diesel'], dtype=pl.Utf8),
            pl.Series("marque", ['CITROEN'], dtype=pl.Utf8),
            pl.Series("modele", ['C3'], dtype=pl.Utf8),
            pl.Series("generation", ['PICASSO phase 2'], dtype=pl.Utf8),
            pl.Series("cylindre", ['1.6'], dtype=pl.Utf8),
            pl.Series("moteur", ['HDI'], dtype=pl.Utf8),
            pl.Series("puissance", [92], dtype=pl.Int64),
            pl.Series("finition", ['EXCLUSIVE'], dtype=pl.Utf8),
            pl.Series("batterie", [None], dtype=pl.Utf8),
        ]
        )
    pred = predict_prix(data_to_predict, "CITROEN")
    assert type(pred) == np.float64

def test_predict_prix_knn():
    data_to_predict = pl.DataFrame(
        [
            pl.Series("annee", [2017], dtype=pl.Int32),
            pl.Series("kilometrage", [63888], dtype=pl.Int64),
            pl.Series("boite", ['Automatique'], dtype=pl.Utf8),
            pl.Series("energie", ['Essence'], dtype=pl.Utf8),
            pl.Series("marque", ['PORSCHE'], dtype=pl.Utf8),
            pl.Series("modele", ['911'], dtype=pl.Utf8),
            pl.Series("generation", ['TYPE 991 CABRIOLET TURBO phase 2'], dtype=pl.Utf8),
            pl.Series("cylindre", ['3.8'], dtype=pl.Utf8),
            pl.Series("moteur", [None], dtype=pl.Utf8),
            pl.Series("puissance", [540], dtype=pl.Int64),
            pl.Series("finition", ['TURBO'], dtype=pl.Utf8),
            pl.Series("batterie", [None], dtype=pl.Utf8),
        ]
        )
    pred = predict_prix(data_to_predict, "PORSCHE")
    assert type(pred) == np.float64


def test_predict_prix_lin_reg():
    data_to_predict = pl.DataFrame(
        [
            pl.Series("annee", [2015], dtype=pl.Int32),
            pl.Series("kilometrage", [57330], dtype=pl.Int64),
            pl.Series("boite", ['Automatique'], dtype=pl.Utf8),
            pl.Series("energie", ['Hybrides'], dtype=pl.Utf8),
            pl.Series("marque", ['LEXUS'], dtype=pl.Utf8),
            pl.Series("modele", ['NX'], dtype=pl.Utf8),
            pl.Series("generation", ['NA'], dtype=pl.Utf8),
            pl.Series("cylindre", ['2.5'], dtype=pl.Utf8),
            pl.Series("moteur", ['300H'], dtype=pl.Utf8),
            pl.Series("puissance", [197], dtype=pl.Int64),
            pl.Series("finition", ['F SPORT'], dtype=pl.Utf8),
            pl.Series("batterie", [None], dtype=pl.Utf8),
        ]
    )
    pred = predict_prix(data_to_predict, "LEXUS")
    assert type(pred) == np.float64
