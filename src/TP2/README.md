# TP2 — Développement d’index pour un moteur de recherche

## Contexte et objectif

Ce TP a pour objectif de **préparer la construction d’un moteur de recherche** en mettant en place différents types d’index à partir du jeu de données de produits collecté dans le TP1.

À partir d’un fichier de produits au format **JSONL**, nous construisons :

* des **index inversés textuels** (titre, description),
* des **index inversés par caractéristiques** (features),
* un **index agrégé des reviews** (non inversé).

## Données d’entrée

* **Fichier** : `input/products.jsonl`
* **Format** : JSON Lines (un document par ligne)
* **Informations disponibles par produit** :

  * URL
  * Titre
  * Description
  * Features du produit (marque, origine, etc.)
  * Reviews (date, note, texte)
  * Liens sortants

Lors du parsing, les informations suivantes sont également extraites depuis l’URL :

* **ID produit**
* **Variante**, si présente (`?variant=...`)

## Prétraitements

Les champs textuels (titre, description, features textuelles) subissent les traitements suivants :

* passage en minuscules,
* suppression de la ponctuation,
* tokenisation par séparation sur les espaces,
* suppression des *stop words* anglais,
* lemmatisation optionnelle (NLTK).

Ces opérations sont implémentées dans le module `utils.py`.

## Index construits

Les index produits sont sauvegardés dans le dossier `output/`.

### 1. Index du titre

* **Type** : index inversé positionnel
* **Structure** :

  ```json
  token → { url → [positions] }
  ```
* **Fichier** : `title_index.json`

### 2. Index de la description

* **Type** : index inversé positionnel
* **Structure** :

  ```json
  token → { url → [positions] }
  ```
* **Fichier** : `description_index.json`

### 3. Index des features

Les caractéristiques du produit sont traitées comme des champs textuels indépendants.

* **Features indexées** :

  * brand
  * origin
* **Type** : index inversé simple
* **Structure** :

  ```json
  token → [url_1, url_2, ...]
  ```
* **Fichiers** :

  * `brand_index.json`
  * `origin_index.json`

### 4. Index des reviews

Les reviews ne sont pas traitées comme du texte inversé mais comme des **données agrégées** permettant le classement des documents.

* **Type** : index non inversé
* **Informations stockées par document** :

  * nombre total de reviews,
  * note moyenne,
  * dernière note (review la plus récente).
* **Fichier** : `reviews_index.json`

## Organisation du code

* `json_parser.py`
  Lecture du fichier JSONL et extraction des identifiants produits.
* `utils.py`
  Fonctions de tokenisation, normalisation et gestion des stop words.
* `index.py`
  Fonctions de création des différents index :

  * titre,
  * description,
  * features,
  * reviews.
* `__init__.py`
  Point d’entrée du TP : génération et sauvegarde de tous les index.

## Installation

Depuis la racine du dépôt :

```bash
pip install -r requirements.txt
```

## Exécution

Depuis le dossier `src/TP2` :

```bash
python __init__.py
```

L’exécution génère automatiquement l’ensemble des fichiers d’index dans le dossier `output/`.

## Choix d’implémentation

* Utilisation d’**index inversés** pour les champs textuels afin de permettre une recherche efficace.
* Séparation claire entre :

  * index lexicaux (titre, description, features),
  * index statistiques (reviews).
* Respect du principe : *une fonction = une responsabilité*.

## Conclusion

Ce TP met en place les briques nécessaires à la construction d’un moteur de recherche :

* indexation lexicale,
* indexation par caractéristiques,
* exploitation des métadonnées de qualité (reviews).
