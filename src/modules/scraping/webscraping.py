import requests as rq
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from pathlib import Path
import json
from dataclasses import dataclass
import time
from serde.json import to_json


def recup_nom_vehicule(annonce: Tag) -> str:
    """
    Récupère le nom du véhicule à partir d'une balise h2 HTML représentant une annonce.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        str: Nom du véhicule extrait de l'annonce.
    """

    nom_vehicule = annonce.find_all(
        "h2",
        class_="Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2",
    )
    return nom_vehicule[0].text


def recup_cylindre(annonce: Tag) -> str:
    """
    Récupère le cylindre à partir d'une Balise HTML d'une annonce de vente de voiture.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        str: Cylindre extrait de l'annonce.
    """

    cylindre = annonce.find_all(
        "div",
        class_="Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2",
    )
    return cylindre[0].text

def recup_caracteristiques(annonce: Tag) -> tuple:
    """
    Récupère les caractéristiques d'une annonce à partir de balises HTML spécifiques.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        tuple: Un tuple contenant l'année, le kilométrage, le type de boîte et le type d'énergie de l'annonce.
    """

    caracteristiques = annonce.find_all(
        "div",
        class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2",
    )
    try:
        annee, kilometrage, boite, energie = [
            caracteristiques[n].text for n in range(len(caracteristiques))
        ]
    except ValueError:
        annee, kilometrage, boite, energie = (
            caracteristiques[0].text,
            caracteristiques[1].text,
            caracteristiques[2].text,
            "erreur",
        )
    return annee, kilometrage, boite, energie


def recup_prix(annonce: Tag) -> str:
    """
    Récupère le prix à partir d'une Balise HTML d'une annonce de vente de voiture.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        str: Prix extrait de l'annonce.
    """

    prix = annonce.find_all(
        "span",
        class_="Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2",
    )
    return prix[0].text


def recup_position_marché(annonce: Tag) -> str:
    """
    Récupère la position sur le marché à partir d'une balise HTML spécifique.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        str: Position sur le marché extraite de l'annonce.
    """

    position_marché = annonce.find_all(
        "div", class_="Text_Text_text Text_Text_bold Text_Text_label2"
    )
    return position_marché[0].text


def recup_garantie(annonce: Tag) -> str:
    """
    Récupère les informations sur la garantie à partir d'une balise HTML spécifique.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        str: Détails sur la garantie extraite de l'annonce, ou "NA" s'il n'y a pas d'informations sur la garantie.
    """

    garanties = annonce.find_all(
        "div", class_="Text_Text_text Text_Text_bold Text_Text_label2"
    )
    if len(garanties) >= 2:
        garantie = str(garanties[1].text)
    else:
        return "NA"
    return garantie


def recup_href(annonce: Tag) -> str:
    """
    Récupère l'url d'une annonce à partir d'une balise HTML spécifique.

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        str: L'url de l'annonce, ou "NA" s'il n'y a pas d'url trouvée.
    """

    href = annonce.find(
        "a",
        attrs={
            "class": "Vehiculecard_Vehiculecard_vehiculeCard Containers_Containers_containers Containers_Containers_borderRadius Containers_Containers_darkShadowWide"
        },
    )
    if isinstance(href, Tag):
        id = "https://www.lacentrale.fr" + str(href.get("href"))
        return id
    else:
        return "NA"

@dataclass
class voiture:
    marque: str
    cylindre: str
    annee: str
    kilometrage: int
    boite: str
    energie: str
    prix: str
    position_marché: str
    garantie: str
    lien: str

def recup_informations_voiture(annonce: Tag) -> voiture:
    """
    Récupère les informations disponibles sur une annonce de véhicule et les renvoie sous forme d'un objet "voiture".

    ## Parameters:
        annonce (Tag): Balise HTML d'une annonce de vente de voiture.

    ## Returns:
        voiture: Objet représentant les informations extraites de l'annonce, telles que la marque, le cylindre,
        l'année, le kilométrage, la boîte de vitesse, le type d'énergie, le prix, la position sur le marché,
        la garantie et le lien.
    """

    marque = recup_nom_vehicule(annonce)
    cylindre = recup_cylindre(annonce)
    annee, kilometrage, boite, energie = recup_caracteristiques(annonce)
    prix = recup_prix(annonce)
    position_marché = recup_position_marché(annonce)
    garantie = recup_garantie(annonce)
    lien = recup_href(annonce)
    return voiture(
        marque=marque,
        cylindre=cylindre,
        annee=annee,
        kilometrage=kilometrage,
        boite=boite,
        energie=energie,
        prix=prix,
        position_marché=position_marché,
        garantie=garantie,
        lien=lien,
    )


@dataclass
class NomMarquesModeles:
    marque: str
    modeles: list[str]

    def __iter__(self):
        yield self.marque
        yield from self.modeles


def import_marques_modeles() -> list:
    """
    Importe les données des marques et leurs modèles associés disponibles à partir d'une fichier JSON et les stocke dans une liste.

    ## Returns:
        list: Liste de tuples représentant chaque marque avec une liste de ses modèles associés.

    ## Exemple:
    fichier json: {
    "Marque A": ["Modèle 1", "Modèle 2"],
    "Marque B": ["Modèle 3", "Modèle 4"]
    }

    >>> [
    ("Marque A", ["Modèle 1", "Modèle 2"]),
    ("Marque B", ["Modèle 3", "Modèle 4"])
    ]
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


def recup_page(numero_page: int, marque: str, modele: str) -> BeautifulSoup:
    """
    Récupère les informations d'une page spécifique.

    ## Parameters:
        numero_page (int): Numéro de la page.
        marque (str): Nom de la marque.
        modele (str): Nom du modèle de véhicule.

    ## Raises:
        rq.ConnectionError: Erreur de connexion en cas d'échec après plusieurs tentatives.

    ## Returns:
        BeautifulSoup: Objet BeautifulSoup contenant le contenu de la page.
    """

    adresse = f"https://www.lacentrale.fr/listing?makesModelsCommercialNames={marque.upper()}%3A{modele.upper()}&options=&page={numero_page}"
    max_attempts = 3  # Nombre maximal de tentatives
    current_attempt = 0

    while current_attempt < max_attempts:
        try:
            requete = rq.get(url=adresse)
            page = BeautifulSoup(requete.content, "html.parser")
            return page
        except rq.ConnectionError as e:
            print(f"Erreur de connexion : {e}")
            print("Tentative de reconnexion...")
            time.sleep(60)
            current_attempt += 1
    print("Échec des tentatives de connexion. Arrêt du programme.")
    raise rq.ConnectionError("Échec des tentatives de connexion.")

def recup_annonces(page: BeautifulSoup) -> ResultSet:
    """
    Récupère les éléments div contenant les informations de chaque annonce pour une page donnée.

    ## Parameters:
        page (BeautifulSoup): L'objet BeautifulSoup de la page HTML analysée.

    ## Returns:
        ResultSet: Une liste qui contient les éléments div contenant les informations de chaque annonce sur la page.
    """
    annonces = page.find_all("div", class_="searchCardContainer")
    return annonces


def recup_data_voitures(annonces: ResultSet) -> list[voiture]:
    """
    Récupère les données de chaque voiture à partir des annonces disponibles.

    ## Parameters:
        annonces (ResultSet): Liste des divs BeautifulSoup représentant les annonces des voitures.

    ## Returns:
        list: Liste d'objets "voiture" (dataclass) contenant les informations extraites de chaque annonce.
    """

    voitures = list()
    for annonce in annonces:
        voitures.append(recup_informations_voiture(annonce))
    return voitures


def print_info_scraping(pages_extraites: int, temps_execution: float) -> None:
    """
    Affiche les informations sur le scraping effectué.

    ## Parameters:
        pages_extraites (int): Nombre total de pages extraites.
        temps_execution (float): Temps total d'exécution en secondes.

    ## Returns:
        None
    """
    if temps_execution != 0:
        pages_par_minute = (pages_extraites / temps_execution) * 60
        info_string = f"Nombre total de pages extraites : {pages_extraites} ||| {pages_par_minute:.2f} pages/min."
        print(info_string, end="\r")
    return None


def extraire_toutes_annonces(
    nombre_pages: int, nom_marques_modeles: NomMarquesModeles
) -> list:
    """
    Récupère toutes les annonces pour une liste de marques et de modèles sur un certain nombre de pages.

    ## Parameters:
        nombre_pages (int): Nombre total de pages extraites pour chaque marque et modèle.
        nom_marques_modeles (NomMarquesModeles): Liste contenant les noms des marques et leurs modèles associés.

    ## Raises:
        rq.ConnectionError : En cas d'erreur de connexion lors de l'extraction.

    ## Returns:
        list: Liste regroupant toutes les annonces extraites.
    """

    liste_annonces = list()
    pages_extraites = 0
    temps_debut = time.time()
    try:
        for i in nom_marques_modeles:
            time.sleep(0.01)
            marque = i.marque
            for modele in i.modeles:
                time.sleep(0.01)
                for num_page in range(1, nombre_pages, 1):
                    page = recup_page(num_page, marque, modele)
                    annonces_page = recup_annonces(page)
                    if annonces_page == []:
                        break
                    else:
                        liste_annonces.append(annonces_page)
                        pages_extraites += 1
                        temps_execution = time.time() - temps_debut
                        print_info_scraping(pages_extraites, temps_execution)
                        if pages_extraites % 2000 == 0:
                            time.sleep(30)
    except rq.ConnectionError:
        print(
            f"""
            \nIl y a eu une erreur au bout de : {pages_extraites + 1} extraites.
            """
        )

    annonces = [
        annonce
        for sous_liste_annonce in liste_annonces
        for annonce in sous_liste_annonce
    ]
    print(f"\nNombre total d'annonces extraites : {len(annonces)}")
    return annonces


def export_to_json(voitures: list[voiture], chemin_sortie: str) -> None:
    """
    Exporte une liste d'objets voiture vers un fichier JSON.

    ## Parameters:
        voitures (list): Liste d'objets de type "voiture" à exporter.
        chemin_sortie (str): Chemin de sortie du fichier JSON.

    ## Returns:
        None
    """
    try:
        voitures_json = to_json(voitures)
        with open(chemin_sortie, "w", encoding="utf-8") as json_file:
            json_file.write(voitures_json)
    except:
        print("Erreur lors de l'exportation en format json.")
        return None


def fusionner_fichiers_json(fichiers_entree: list[str]) -> list[dict]:
    """
    Fusionne les données de plusieurs fichiers JSON en une seule liste de dictionnaires.

    ## Parameters:
        fichiers_entree (list[str]): Liste des chemins des fichiers JSON en entrée.

    ## Returns:
        list[dict]: Liste regroupant les données de tous les fichiers JSON.
    """
    if not isinstance(fichiers_entree, list):
        raise TypeError("L'argument doit être une liste.")

    elif len(fichiers_entree) >= 1:
        try:
            donnees_finales = []
            for fichier_entree in fichiers_entree:
                with open("json/" + fichier_entree, "r", encoding="utf-8") as file:
                    donnees_fichier = json.load(file)
                    donnees_finales.extend(donnees_fichier)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Impossible d'importer les fichiers spécifiés. Vérifiez que le dossier 'json' existe bien et qu'il contient bien les fichiers renseignés."
            )
    elif len(fichiers_entree) == 0:
        raise ValueError("La liste ne doit pas être vide.")

    return donnees_finales
