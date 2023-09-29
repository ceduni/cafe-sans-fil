# API avec FastAPI

## Développement

- On utilise un environnement virtuel pour éviter les conflits avec les dépendances, et ne pas avoir à les installer globalement
- Il a été créé avec `python -m venv env`, cela crée un dossier `env` avec les fichiers nécessaires
- Pour l'activer, il faut faire `source ./env/bin/activate` sur Linux, macOS ou `.\env\Scripts\Activate.ps1` avec Windows PowerShell
- Une fois activé, `(env)` s'affichera désormais avant les commandes dans le terminal
- Pour le désactiver, il faut entrer `deactivate`

> **Note:** Il faut **toujours** activer l'environnement virtuel avant de lancer le serveur ou d'installer des dépendances

## Installation

- Avoir installé Python 3.7+ et pip (on s'assure que pip est à jour avec `python -m pip install --upgrade pip`)
- Avoir installé les dépendances avec `pip install -r requirements.txt`
- Lancer le serveur avec `uvicorn main:app --reload`

> La commande uvicorn main:app réfère à: - main: le fichier main.py (le module Python) - app: l'objet créé dans main.py avec la ligne app = FastAPI() - --reload fait restart le serveur à chaque changement dans le code, à utiliser en développement seulement!

- L'api sera disponible à [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Une documentation automatique de l'API est disponible à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Avancée du développement

#### 2023-09-29

- On a initialisé le projet avec FastApi, et créé un environnement virtuel pour la gestion des dépendances, en suivant la documentation
- On ajoute chaque dépendance et leur version dans le fichier `requirements.txt` au fur et à mesure
- On a installé un serveur de production (Uvicorn, recommandé par la doc de FastAPI)
- On a créé un fichier `main.py` qui contient le code de l'API (pour tester pour l'instant)

## Ressources utilisées

- [FastAPI](https://fastapi.tiangolo.com/#requirements)
- [Aide par rapport au setup du venv](https://fastapi.tiangolo.com/contributing/#virtual-environment-with-venv)
- [First steps FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)
