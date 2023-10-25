# Back-end de Café sans-fil

## Prérequis

- Assurez-vous d'avoir installé Python 3.10.
- Si vous n'avez pas `pipenv`, installez-le avec `pip install pipenv`.

## Configuration du fichier .env

Pour configurer le fichier .env dans le backend, créez un fichier nommé .env dans `/back/app`. Ajoutez ce qui suit dans le fichier .env :

```
JWT_SECRET_KEY=<RAMDOM_STRING>
JWT_REFRESH_SECRET_KEY=<RANDOM_SECTURE_LONG_STRING>
MONGO_CONNECTION_STRING=<MONGO_DB_CONNECTION_STRING>
```

> **Note importante:** Les valeurs `<RAMDOM_STRING>`, `<RANDOM_SECTURE_LONG_STRING>` et `<MONGO_DB_CONNECTION_STRING>` sont des espaces réservés. Vous devez les remplacer par vos propres valeurs avant de déployer ou d'exécuter le backend.

## Installation

- On utilise `pipenv` pour gérer les dépendances et l'environnement virtuel du projet.
- Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
- Installez les dépendances nécessaires avec `pipenv install -r requirements.txt`.
- Lancez le serveur avec `uvicorn app.main:app --reload`.

> **Note:** La commande `uvicorn app.main:app` réfère à: 
> - `app.main`: le fichier `main.py` dans le dossier `app` (le module Python).
> - `app`: l'objet créé dans `main.py` avec la ligne `app = FastAPI()`.
> - `--reload` fait redémarrer le serveur à chaque changement dans le code, à utiliser en développement seulement!

- L'api sera disponible à [http://127.0.0.1:8000](http://127.0.0.1:8000).
- Une documentation automatique de l'API est disponible à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

> Pour quitter l'environnement virtuel, utilisez la commande `exit`.

## Avancée du développement

#### 2023-10-25

- Ajout de vérifications d'autorisation pour les rôles.

#### 2023-10-24

- Ajout des routes d'authentification (login, test-token, refresh).
- Mise à jour des schémas pour la validation des requêtes et des réponses.

#### 2023-10-21

- Mise à jour de la recherche: Inclusion des descriptions, facultés, localisations et filtres.
- Ajout de la récupération des commandes pour l'utilisateur/le café avec filtrage de statut.
- Ajout de paramètres de filtrage supplémentaires.

#### 2023-10-20

- Refactorisation de la structure Backend et API.
- Mise à jour majeure de l'API: Ajout des fonctionnalités CRUD pour les cafés et les éléments de menu, ainsi que leurs modèles, schémas et services associés.
- Connexion à la base de données cloud Atlas et population avec des données initiales.
- Ajout d'une fonctionnalité de recherche unifiée pour les cafés et les éléments de menu.
- Ajout de docstrings aux modules backend.

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
- [First steps FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Getting started MongoDB FastAPI](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)
- [How to use FastAPI with MongoDB](https://plainenglish.io/blog/how-to-use-fastapi-with-mongodb-75b43c8e541d)
- [Using FastAPI to Build Python Web APIs – Real Python](https://realpython.com/fastapi-python-web-apis/)
- [FARM Stack Course - FastAPI, React, MongoDB](https://www.youtube.com/watch?v=OzUzrs8uJl8&list=PLAt-l74BsucNBwFANkqwisPMSLE62rKG_&index=2&t=2912s&ab_channel=freeCodeCamp.org)
- [The ultimate FARM stack Todo app with JWT PART I - FastAPI + MongoDB | abdadeel](https://www.youtube.com/watch?v=G8MsHbCzyZ4&ab_channel=ABDLogs)
- [How to build a FastAPI app with PostgreSQL](https://www.youtube.com/watch?v=398DuQbQJq0)
- [How to create an API in Python](https://anderfernandez.com/en/blog/how-to-create-api-python/)

## Difficulités rencontrées

- Il a fallu spécifiquement installer pydantic 1.9 au lieu de la dernère version, car la v2 a causé des erreurs avec MongoDB et les BaseModel utilisant des ObjectId. De plus, la documentation officielle de MongoDB n'utilise pas la v2. (voir [ici](https://www.mongodb.com/community/forums/t/pydantic-v2-and-objectid-fields/241965)).  

- Un problème rencontré sur MacBook était l'erreur "command not found" après avoir installé pipenv. La solution a été trouvée dans cette [vidéo](https://www.youtube.com/watch?v=Bzn_MZ0tNXU&ab_channel=SpecialCoder).