# API avec FastAPI

## Développement

- On utilise un environnement virtuel pour éviter les conflits avec les dépendances, et ne pas avoir à les installer globalement
- Il a été créé avec `python -m venv env`, cela crée un dossier `env` avec les fichiers nécessaires
- Pour l'activer, il faut faire `source ./env/bin/activate` sur Linux, macOS ou `.\env\Scripts\Activate.ps1` avec Windows PowerShell
- Une fois activé, `(env)` s'affichera désormais avant les commandes dans le terminal
- Pour le désactiver, il faut entrer `deactivate`

> **Note:** Après avoir installé des dépendances, il faut les ajouter au fichier `requirements.txt` avec la commande `pip freeze > requirements.txt`

> **Note:** Il faut **toujours** activer l'environnement virtuel avant de lancer le serveur ou d'installer des dépendances

## Installation

- Avoir installé Python 3.7+ et pip (on s'assure que pip est à jour avec `python -m pip install --upgrade pip`)
- Avoir créé en local un environnement virtuel nommé `env` avec la commande indiquée dans la section Développement
- Avoir activé l'environnement virtuel avec la commande indiquée dans la section Développement
- Avoir installé les dépendances avec `pip install -r requirements.txt`, **dans l'environnement virtuel**
- Lancer le serveur avec `uvicorn main:app --reload`, **dans l'environnement virtuel**

> La commande uvicorn main:app réfère à: - `main`: le fichier main.py (le module Python) - `app`: l'objet créé dans main.py avec la ligne `app = FastAPI()` - `--reload` fait restart le serveur à chaque changement dans le code, à utiliser en développement seulement!

- L'api sera disponible à [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Une documentation automatique de l'API est disponible à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Avancée du développement

#### 2023-10-04

- On a créé un fichier `models.py` qui contient des premiers modèles de données
- On a crée des premières routes test, testables avec Postman

#### 2023-09-29

- On a initialisé le projet avec FastAPI, et créé un environnement virtuel pour la gestion des dépendances, en suivant la documentation
- On ajoute chaque dépendance et leur version dans le fichier `requirements.txt` au fur et à mesure
- On a installé un serveur de production (Uvicorn, recommandé par la doc de FastAPI)
- On a créé un fichier `main.py` qui contient le code de l'API (pour tester pour l'instant)

## Ressources utilisées

- [FastAPI](https://fastapi.tiangolo.com/#requirements)
- [Aide par rapport au setup du venv](https://fastapi.tiangolo.com/contributing/#virtual-environment-with-venv)
- [First steps FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Getting started MongoDB FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)
- [How to use FastAPI with MongoDB](https://plainenglish.io/blog/how-to-use-fastapi-with-mongodb-75b43c8e541d)
- [Using FastAPI to Build Python Web APIs – Real Python](https://realpython.com/fastapi-python-web-apis/)

## Difficulités rencontrées

- Il a fallu spécifiquement installer pydantic 1.9 au lieu de la dernère version, car la v2 a causé des erreurs avec MongoDB et les BaseModel utilisant des ObjectId. De plus, la documentation officielle de MongoDB n'utilise pas la v2. (voir [ici](https://www.mongodb.com/community/forums/t/pydantic-v2-and-objectid-fields/241965)).