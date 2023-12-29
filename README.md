# Scraping & Machine Learning project

<p align="center">
  <img src="https://media.tenor.com/pM_ncMFQOeoAAAAC/lightning-mcqueen.gif" />
</p>

Scraping des annonces de vente de voiture d'occasion sur le site de [lacentrale.fr](https://www.lacentrale.fr).

Le scraping fonctionne essentiellement à l'aide de [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) et à partir de requêtes 'https'. 

### Comment procéder :


-  On récupère tous les noms de marques et modèles présent sur le site.
-  On effectue le scraping à partir de requête https en modifiant l'url par rapport à la marque et au modèle. Ce faisant, on extrait le maximum de données pour chaque type de véhicule.
-  On nettoie la base en faisant attention à d'eventuelle doublons et on la met sous le format choisi (ex : pandas, polars etc..).
-  On teste différents modèles de Machine Learning, on optimise les paramêtres et on choisi le meilleur des modèles.
-  On met en prod, et on construit une application autour de ça (ex : application qui donne une estimation de la valeur du véhicule).

### TO DO LIST :

#### Scraping
- Scraper toutes les annonces sur le site : Done
- Réussir à parser les données dans une table et nettoyer la base : Done

#### Machine Learning

- Faire du pre-processing : Nettoyer la base de données pour avoir une base avec le moins de NA possible (important pour la partie machine learning)
- Faire n modèles pour n marques, en prenant en compte les marques avec le plus de données : En cours
- Choisir le meilleur et le sauvegarder : Done

#### Application
- Faire une application estimateur de prix + autre idée. : En cours
- Trouver un moyen pour ne pas avoir à charger la base de données à chaque action de l'utilisateur (base SQL ?) : Done
- Avoir un interface épurée avec une partie recherche d'annonce : En cours
- Faire la partie estimateur de prix, si données manquantes à l'entrée, proposer plusieurs estimation (via graph plotly par exemple) : A faire
