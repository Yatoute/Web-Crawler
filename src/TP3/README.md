# TP3 — Moteur de recherche


## Objectif du TP

Ce troisième TP constitue la **suite et l’aboutissement des TP1 et TP2**.
L’objectif est de mettre en œuvre un **moteur de recherche complet** reposant sur :

* les index construits au TP2 ;
* une phase de **requêtage** (prétraitement, filtrage de documents) ;
* un **modèle de ranking linéaire** combinant plusieurs signaux de pertinence ;
* la restitution des **produits les mieux classés** pour une requête donnée.


## Organisation du projet

```
TP3
├── config.py
├── __init__.py
├── input
│   ├── title_index.json
│   ├── description_index.json
│   ├── brand_index.json
│   ├── origin_index.json
│   ├── origin_synonyms.json
│   ├── reviews_index.json
│   └── products.jsonl
├── output
│   ├── MagicSteps.json
│   ├── chocolate_candy.json
│   └── sneakers_usa.json
├── quering.py
├── ranking.py
├── search_engine.py
└── utils.py
```


## Description des composants

### 1. Prétraitement et requêtage (`quering.py`)

* Tokenisation et normalisation des requêtes utilisateur ;
* Expansion simple par synonymes (ex. pays d’origine) ;
* Sélection de documents candidats via :

  * filtrage **OR** (au moins un token),
  * ou filtrage **AND** (tous les tokens).


### 2. Fonctions de ranking (`ranking.py`)

Les scores de pertinence implémentés sont :

* **BM25** par champ (title, description) ;
* **Exact Match Score** : proportion de tokens de la requête présents dans le document ;
* **Reviews Score** : score basé sur la note moyenne des avis utilisateurs.

Ces signaux sont combinés à l’aide d’un **modèle de ranking linéaire** :

score(d, q) = Σ_i w_i · s_i(d, q)


où ( s_i ) représente un signal de pertinence et ( w_i ) son poids.


### 3. Moteur de recherche (`search_engine.py`)

La classe `SearchEngine` orchestre l’ensemble du pipeline :

1. Chargement des index (lazy loading) ;
2. Préparation de la requête ;
3. Sélection des documents candidats ;
4. Calcul du score de ranking ;
5. Lecture du fichier `products.jsonl` ;
6. Restitution des produits classés, enrichis de leur score.


## Exécution

L’exécution principale se fait via le fichier `__init__.py` :

```bash
python __init__.py
```

Trois requêtes exemples sont exécutées automatiquement :

* `brand MagicSteps`
* `box of chocolate candy`
* `Light-Up Sneakers made in america`

Les résultats sont écrits dans le dossier `output/` au format JSON.


## Résultats

Chaque fichier de sortie contient une liste de produits classés par ordre décroissant de pertinence, avec un champ supplémentaire :

```json
"_score": <score de ranking>
```
