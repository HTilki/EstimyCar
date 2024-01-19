"""Module de test sur l'application streamlit
"""

from streamlit.testing.v1 import AppTest
from streamlit.testing.v1.element_tree import UnknownElement

def test_lancement_app():
    at = AppTest.from_file("streamlit_app.py").run()
    assert not at.exception   

def test_user_role_a():
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Acheteur").run(timeout=5)
    assert not at.exception 

def test_user_role_v():
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    assert not at.exception 

def test_show_data_frame():
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Acheteur").run(timeout=5)
    assert at.tabs[0].dataframe.values

def test_prediction_prix_pred():
    # permet de tester si la prédiction fonctionne bien même avec des données manquantes en entrée
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    at.sidebar.selectbox(key="marque_select").set_value("PORSCHE").run(timeout=5)
    at.button[0].click().run()
    assert isinstance(at.session_state["prix_pred"], float)
    assert at.session_state["prix_pred"] != 0

def test_prediction_prix_moy():
    # permet de tester si on trouve bien un prix moyen
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    at.sidebar.selectbox(key="marque_select").set_value("CITROEN").run(timeout=5)
    at.sidebar.selectbox(key="modele_select").set_value("C3").run(timeout=5)
    at.sidebar.selectbox(key="cylindre_select").set_value("1.2").run(timeout=5)
    at.sidebar.number_input[0].set_value(83).run(timeout=5)
    at.sidebar.number_input[1].set_value(9000).run(timeout=5)
    at.sidebar.selectbox(key="boite_select").set_value("Manuelle").run(timeout=5)
    at.sidebar.selectbox(key="energie_select").set_value("Essence").run(timeout=5)
    at.button[0].click().run()
    assert isinstance(at.session_state["prix_moy_pred"], float)
    assert at.session_state["prix_moy_pred"] != 0

def test_prediction_erreur_pred():
    # Test si il y a bien le message d'erreur qui s'affiche lorsqu'il n'est pas possible d'effectuer la prédiction
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    at.sidebar.selectbox(key="marque_select").set_value("FERRARI").run(timeout=5)
    at.sidebar.selectbox(key="modele_select").set_value("208").run(timeout=5)
    at.sidebar.selectbox(key="energie_select").set_value("Électrique").run(timeout=5)
    at.button[0].click().run(timeout=5)
    assert at.metric.values[0] == "Erreur lors de l'estimation du prix."

def test_prediction_erreur_prix_moy():
    # ici on test si on renvoie bien Prix moyen indisponible quand il n'y a aucun véhicule qui correspond
    # ici l'exemple est une PORSCHE 911 de 2024 avec un kilometrage de 900000 (impossible)
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    at.sidebar.selectbox(key="marque_select").set_value("PORSCHE").run(timeout=5)
    at.sidebar.selectbox(key="modele_select").set_value("911").run(timeout=5)
    at.sidebar.select_slider(key="annee_single_slider").set_value(2024).run(timeout=5)
    at.sidebar.number_input[1].set_value(900000).run(timeout=5)
    at.button[0].click().run()
    assert at.metric.values[1] == "Prix moyen indisponible."

def test_prediction_km_plot_1():
    # Test si il y a bien le graphique qui s'affiche
    # ici UnkownElement est la class du graphique plotly qui s'affiche
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    at.sidebar.selectbox(key="marque_select").set_value("PORSCHE").run(timeout=5)
    at.sidebar.selectbox(key="modele_select").set_value("356").run(timeout=5)
    at.button[1].click().run(timeout=5)
    assert isinstance(at.get("plotly_chart")[0], UnknownElement)



def test_prediction_km_plot_2():
    # Test si il y a bien le message d'erreur qui s'affiche lorsqu'il n'est pas possible de generer le graphique
    at = AppTest.from_file("streamlit_app.py").run(timeout=5)
    at.sidebar.selectbox(key="user_role_select").set_value("Vendeur").run(timeout=5)
    at.sidebar.selectbox(key="marque_select").set_value("FERRARI").run(timeout=5)
    at.sidebar.selectbox(key="modele_select").set_value("208").run(timeout=5)
    at.sidebar.selectbox(key="energie_select").set_value("Électrique").run(timeout=5)
    at.button[1].click().run(timeout=5)
    assert at.error.values[0] == "Erreur lors de la génération du graphique. Vérifiez que toutes les caractéristiques sont bien renseignées."

