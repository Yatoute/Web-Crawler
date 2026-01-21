# TP1 — Web Crawling

## Objectif du TP

Ce premier TP a pour objectif de mettre en œuvre un **crawler web simple**, respectueux des règles d’exploration, afin de collecter des pages produits à partir d’un site e-commerce fictif.

Il constitue la **première étape de la chaîne complète** développée au cours des TP :

* **TP1** : collecte des données (crawling),
* **TP2** : indexation des contenus collectés,
* **TP3** : recherche et ranking des documents.

## Installation

Les dépendances Python sont communes à l’ensemble du projet et se trouvent à la racine du dépôt.

```bash
pip install -r requirements.txt
```

## Organisation du projet

```
TP1
├── crawler.py
├── html_parser.py
├── http_client.py
├── robots.py
├── __init__.py
└── outputs
    └── products.json
```

## Description des composants

### 1. Crawler (`crawler.py`)

Le crawler implémente :

* une **file d’attente d’URLs** à visiter ;
* une **priorisation** des URLs contenant un mot-clé (par défaut `product`) ;
* une **limite sur le nombre de pages crawlées** ;
* une **temporisation (`sleep`)** entre deux requêtes ;
* un mécanisme de **déduplication** des URLs.

Le crawler respecte les règles définies dans le fichier `robots.txt`.

### 2. Client HTTP (`http_client.py`)

* Envoi de requêtes HTTP avec un **User-Agent explicite** ;
* Gestion simple des erreurs réseau.

### 3. Parser HTML (`html_parser.py`)

Extraction des informations suivantes à partir des pages HTML :

* URL canonique ;
* titre ;
* description ;
* caractéristiques produit ;
* liens sortants ;
* avis utilisateurs (au format JSON embarqué).

### 4. Gestion du robots.txt (`robots.py`)

* Téléchargement et parsing du fichier `robots.txt` ;
* Application des règles `Allow` / `Disallow` selon le User-Agent ;
* Autorisation par défaut en cas d’indisponibilité du fichier.

## Exécution

Le crawler est lancé via le fichier `__init__.py` :

```bash
python __init__.py
```

Le crawling démarre à partir de l’URL :

```
https://web-scraping.dev/products
```

Les données collectées sont enregistrées dans :

```
outputs/products.json
```


## Résultat

Le fichier `products.json` contient une liste de documents JSON représentant les pages crawlées, incluant :

* les métadonnées de la page ;
* les caractéristiques produit ;
* les liens ;
* les avis utilisateurs.

Ces données servent ensuite d’entrée pour le **TP2 (indexation)**.
