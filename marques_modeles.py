from bs4 import BeautifulSoup
from pathlib import Path

def recup_marques_modeles() -> dict:
    page_accueil = Path(".").resolve() / "pages/page_accueil.html"
    page = BeautifulSoup(page_accueil.read_text(encoding="utf8"))
    div_voitures = page.find('div', class_='dropdown__itemsWrapper')

    # Initialize an empty dictionary to store brand and model information
    marques_modeles = {}

# Iterate through the divs containing brand information
    for marque_div in div_voitures.find_all('div', class_='dropdown__itemsWrapper__brand-name'):
        # Extract the brand name
        nom_marque = marque_div.text.strip()
        
        # Find the divs containing model information for this brand using find_next_siblings
        modeles_divs = marque_div.find_next_siblings('div', class_='dropdown__itemsWrapper__model-name')
        
        # Extract all available models for the brand
        modeles = []
        for modele_div in modeles_divs:
            labels = modele_div.find_all('label', class_='Text_Text_text Controls_Controls_label Controls_Controls_right Controls_Controls_active Text_Text_label2')
            modeles.extend(label.text.strip() for label in labels)
        
        # Store the brand and model information in the dictionary
        marques_modeles[nom_marque] = modeles
    return(marques_modeles)