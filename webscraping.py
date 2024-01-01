import requests as rq
from bs4 import BeautifulSoup
from bs4.element import Tag
from pathlib import Path
import json
from dataclasses import dataclass
import time
from serde.json import to_json


def recup_nom_vehicule(annonce : str): 
    """
    Récupère le nom du véhicule à partir d'une balise h2 HTML représentant une annonce.

    ## Parameters:
        annonce (str): Chaîne de balises HTML représentant une annonce. 
        Ex : <h2 class="Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2" style="--textColor: var(--lcui-black);">RENAULT CAPTUR II</h2>

    ## Returns:
        str: Nom du véhicule extrait de l'annonce.
    """

    nom_vehicule = annonce.find_all('h2', class_='Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2')
    return nom_vehicule[0].text


# pour recuperer la cylindré / modele 
def recup_cylindre(annonce : str): 
    """
    Récupère le cylindre à partir d'une chaîne de balises HTML représentant une annonce.
    
    ## Parameters:
        annonce (str): Chaîne de balises HTML représentant une annonce. 
        Ex : <div class="Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2" style="--textColor: var(--lcui-greyDark);">1.3 HYBRID 140 TECHNO</div>

    ## Returns:
        str: Cylindre extrait de l'annonce.
    """

    cylindre = annonce.find_all('div', class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2')
    return cylindre[0].text


# faire la gestion d'erreur ! souvent le type d'energie est manquant, à vérifier !
def recup_caracteristiques(annonce : str): 
    """
    Récupère les caractéristiques d'une annonce à partir de balises HTML spécifiques.

    ## Parameters:
        annonce (str): Chaîne de balises HTML représentant une annonce.
        Ex: <div class="Vehiculecard_Vehiculecard_characteristics"><div class="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2" style="--textColor: var(--lcui-black);">2022</div>
        <div class="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2" style="--textColor: var(--lcui-black);">10 km</div>
        <div class="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2" style="--textColor: var(--lcui-black);">Manuelle</div>
        <div class="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2" style="--textColor: var(--lcui-black);">Essence</div></div>

    ## Returns:
        tuple: Un tuple contenant l'année, le kilométrage, le type de boîte et le type d'énergie de l'annonce.
    """

    caracteristiques = annonce.find_all('div', class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')
    try :
        annee, kilometrage, boite, energie = [caracteristiques[n].text for n in range(len(caracteristiques))]
    except ValueError: 
        annee, kilometrage, boite, energie = caracteristiques[0].text,caracteristiques[1].text,caracteristiques[2].text, "erreur"
    return annee, kilometrage, boite, energie



def recup_prix(annonce : str): 
    """
    Récupère le prix à partir d'une chaîne de balises HTML représentant une annonce.
    
    ## Parameters:
        annonce (str): Chaîne de balises HTML représentant une annonce. 
        Ex: <span class="Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2" style="--textColor: var(--lcui-black);">23 980 €</span>

    ## Returns:
        str: Prix extrait de l'annonce.
    """

    prix = annonce.find_all('span', class_='Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2')
    return prix[0].text



def recup_position_marché(annonce : str): 
    """
    Récupère la position sur le marché à partir d'une balise HTML spécifique.

    ## Parameters:
        annonce (str): Chaîne de balises HTML représentant une annonce.
        Ex: <div class="Text_Text_text Text_Text_bold Text_Text_label2">Bonne affaire</div>

    ## Returns:
        str: Position sur le marché extraite de l'annonce.
    """

    position_marché = annonce.find_all('div', class_='Text_Text_text Text_Text_bold Text_Text_label2')
    return position_marché[0].text



def recup_garantie(annonce : str): 
    """
    Récupère les informations sur la garantie à partir d'une balise HTML spécifique.

    ## Parameters:
        annonce (str): Chaîne de balises HTML représentant une annonce.
        Ex: <div class="Text_Text_text Text_Text_bold Text_Text_label2">Garantie 12 mois</div>

    ## Returns:
        str: Détails sur la garantie extraite de l'annonce, ou "NA" s'il n'y a pas d'informations sur la garantie.
    """

    garantie = annonce.find_all('div', class_='Text_Text_text Text_Text_bold Text_Text_label2')
    if (len(garantie) == 2):
        garantie = garantie[1].text
    else:
        garantie = "NA"
    return garantie



def recup_href(annonce):
    """
    Récupère l'url d'une annonce à partir d'une balise HTML spécifique.

    ## Parameters:
        annonce (str): Balise HTML représentant une annonce.
    
    ## Returns:
        str: L'url de l'annonce, ou "NA" s'il n'y a pas d'url trouvée.
    """

    href = annonce.find("a", attrs={"class":"Vehiculecard_Vehiculecard_vehiculeCard Containers_Containers_containers Containers_Containers_borderRadius Containers_Containers_darkShadowWide"})
    if isinstance(href, Tag):
        id = "https://www.lacentrale.fr" + href.get("href")
        return id
    else:
        return "NA"

# Création de la dataclass
@dataclass
class voiture: 
    marque: str
    cylindre: str
    annee: str
    kilometrage: int
    boite: str
    energie: str
    prix: int
    position_marché: str
    garantie: str
    lien: str


# Fonction permettant de recuperer toutes les informations disponible sur une annonce.
def recup_informations_voiture(annonce: str) -> voiture:
    """
    Récupère les informations disponibles sur une annonce de véhicule et les renvoie sous forme d'un objet "voiture".

    ## Parameters:
        annonce (str): Chaîne de caractères représentant une annonce.

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
        lien=lien
    )


@dataclass
class NomMarquesModeles:
        marque: str
        modeles: list

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
    with open(Path(".").resolve() / "json/marques_modeles.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    for marque, modeles in data.items():
            nom_marques_modeles_list.append(NomMarquesModeles(marque=marque, modeles=modeles))
    return(nom_marques_modeles_list)



def traitement_modele_url(modele) -> str:
    """_summary_

    Args:
        modele (_type_): _description_

    Returns:
        str: _description_
    """
    modele = modele.upper()
    if " " in modele:
        # If it contains spaces, replace them with "%20"
        modele = modele.replace(" ", "%20")
    else:
        # If it doesn't contain spaces, no modification is needed
        modele = modele
    return modele



# Fonction qui récupère les informations d'une page spécifique
def recup_page(numero_page, marque, modele):
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
    #rajouter de la gestion d'erreur en fonction du nombre de page et donc si la requete http marche.
    adresse = f"https://www.lacentrale.fr/listing?makesModelsCommercialNames={marque.upper()}%3A{traitement_modele_url(modele)}&options=&page={numero_page}"
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
            time.sleep(60)  # Pause de 1 minute entre les tentatives
            current_attempt += 1
    print("Échec des tentatives de connexion. Arrêt du programme.")
    raise rq.ConnectionError("Échec des tentatives de connexion.")



# Fonction qui récupère les div qui contienent les informations de chaque annonce pour une page
def recup_annonces(page):
    """
    Récupère les éléments div contenant les informations de chaque annonce pour une page donnée.

    ## Parameters:
        page (BeautifulSoup): L'objet BeautifulSoup de la page HTML analysée.

    ## Returns:
        list: Une liste des éléments div contenant les informations de chaque annonce sur la page.
    """
    annonces = page.find_all('div', class_='searchCardContainer')
    return annonces



def recup_data_voitures(annonces):
    """
    Récupère les données de chaque voiture à partir des annonces disponibles.

    ## Parameters:
        annonces (list): Liste des divs BeautifulSoup représentant les annonces des voitures.

    ## Returns:
        list: Liste d'objets "voiture" (dataclass) contenant les informations extraites de chaque annonce.
    """
    voitures = list()
    for annonce in annonces:
        voitures.append(recup_informations_voiture(annonce))
    return voitures



def print_info_scraping(pages_extraites, temps_execution):
    """
    Affiche les informations sur le scraping effectué.

    ## Parameters:
        pages_extraites (int): Nombre total de pages extraites.
        temps_execution (float): Temps total d'exécution en secondes.

    ## Returns:
        None
    """
    if temps_execution == 0:
        return 0
    else:
        pages_par_minute = (pages_extraites / temps_execution) * 60
        info_string = f"Nombre total de pages extraites : {pages_extraites} ||| {pages_par_minute:.2f} pages/min."
        print(info_string, end='\r')



def extraire_toutes_annonces(nombre_pages, nom_marques_modeles) -> list:
    """
    Récupère toutes les annonces pour une liste de marques et de modèles sur un certain nombre de pages.

    ## Parameters:
        nombre_pages (int): Nombre total de pages extraites pour chaque marque et modèle.
        nom_marques_modeles (list): Liste contenant les noms des marques et leurs modèles associés.

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
                        temps_execution = time.time()-temps_debut
                        print_info_scraping(pages_extraites, temps_execution)
                        if pages_extraites % 2000 == 0:
                            time.sleep(30)
    except rq.ConnectionError:
        print(f"""
            \nIl y a eu une erreur au bout de : {pages_extraites + 1} extraites.
            \nIl faut reprendre l'extraction à : {marque}, {modele}, page : {num_page}
            """)
        return annonces
    #pour ne pas avoir une liste de liste mais une liste unique qui regroupe toutes les annonces
    annonces = [annonce for sous_liste_annonce in liste_annonces for annonce in sous_liste_annonce]
    print(f"\nNombre total d'annonces extraites : {len(annonces)}")
    return annonces



def export_to_json(voitures: voiture, chemin_sortie: str):
    """
    Exporte une liste d'objets voiture vers un fichier JSON.

    ## Parameters:
        voitures (list): Liste d'objets de type "voiture" à exporter.
        chemin_sortie (str): Chemin de sortie du fichier JSON.

    ## Returns:
        None
    """
    try : 
        voitures_json = to_json(voitures)
        with open(chemin_sortie, "w", encoding="utf-8") as json_file:
            json_file.write(voitures_json)
    except:
        print("Erreur lors de l'exportation en format json.")
        return None



def fusionner_fichiers_json(fichiers_entree):
    """
    Fusionne les données de plusieurs fichiers JSON en une seule liste de dictionnaires.

    ## Parameters:
        fichiers_entree (list[str]): Liste des chemins des fichiers JSON en entrée.

    ## Returns:
        list[dict]: Liste regroupant les données de tous les fichiers JSON.
    """
    # Liste pour stocker les données de tous les fichiers JSON
    donnees_finales = []

    # Lire chaque fichier d'entrée et ajouter ses données à la liste
    for fichier_entree in fichiers_entree:
        with open("json/" + fichier_entree, 'r', encoding='utf-8') as file:
            donnees_fichier = json.load(file)
            donnees_finales.extend(donnees_fichier)

    return donnees_finales