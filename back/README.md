# Backend

Le backend de Café sans-fil repose principalement sur **FastAPI** (framework Python) pour le traitement des requêtes (API) et **MongoDB** pour la gestion des données. Actuellement, le déploiement de cette infrastructure s'effectue via la plateforme **Render**.

- [Backend](#backend)
  - [Structure: organisation des fichiers](#structure-organisation-des-fichiers)
  - [Prise en main du code](#prise-en-main-du-code)
  - [Prérequis](#prérequis)
    - [Configuration du fichier `.env`](#configuration-du-fichier-env)
  - [Démarrage du serveur](#démarrage-du-serveur)
  - [Initialisation de la base de données](#initialisation-de-la-base-de-données)
  - [Exécuter les tests](#exécuter-les-tests)
- [Déploiement et Hébergement](#déploiement-et-hébergement)
  - [Service web (API)](#service-web-api)
  - [Application web](#application-web)

  
## Structure: organisation des fichiers

Les fichiers sont organisés suivant la structure suivante:

```ada
/ -- Racine du projet (/back)
├── app/ -- Code source de l'API
│   ├── api/ -- Définit les routes et les points de terminaison de l'API.
│   ├── core/ -- Contient les paramètres de configuration et les utilitaires liés à la sécurité.
│   ├── models/ -- Modèles de schéma de base de données pour l'ORM.
│   ├── schemas/ -- Modèles Pydantic pour la validation et la sérialisation des requêtes/réponses.
│   ├── services/ -- Couche de logique métier, interface entre l'API et la base de données.
│   └── .env
│   └── main.py -- Point d'entrée pour l'application FastAPI, inclut la configuration de l'application.
├── test/ -- Test unitaire
│   └── conftest.py -- Configuration des fixtures de test pour pytest.
│   └── test_auth.py
│   └── test_cafe.py
│   └── test_order.py
│   └── test_user.py
├── utils/
│   ├── templates/ -- Modèles d'email et fichiers json pour l'initialisation des données.
│   │   └── cafes_updated.json
│   │   └── menu_items.json
│   │   └── photo_urls.json
│   │   └── register_mail.html
│   │   └── reset_password_mail.html
│   └── generate_all.py -- Utilitaire pour générer des données d'exemple pour toute l'application.
│   └── generate_cafe.py
│   └── generate_order.py
│   └── generate_user.py
└── log.txt
└── Pipfile
└── requirements.txt
```

## Prise en main du code

## Prérequis

- Assurez-vous d'avoir installé Python 3.11+
  - Si vous n'avez pas `pipenv`, installez-le avec `pip install pipenv`.
- Assurez-vous que MongoDB est installé sur votre système.

### Configuration du fichier `.env`

>  Le fichier `.env` est utilisé pour stocker des variables d'environnement afin de garder les valeurs sensibles et les configurations spécifiques à l'environnement hors du code source et de faciliter la configuration de l'application.

Pour configurer le fichier `.env` dans le backend, créez un fichier nommé `.env` dans `/back/app` avec le contenu suivant:

```ini
JWT_SECRET_KEY=<RAMDOM_STRING>
JWT_REFRESH_SECRET_KEY=<RANDOM_SECURE_LONG_STRING>
BACKEND_CORS_ORIGINS=<BACKEND_CORS_ORIGINS> # "http://localhost:5173" <-- for local running instances
BASE_URL=<BASE_URL> # "http://localhost:8000" <-- for local running instances
MONGO_CONNECTION_STRING=<MONGO_DB_CONNECTION_STRING> # "mongodb://localhost:27017/" <-- for local running instances
MONGO_DB_NAME="cafesansfil"
```

💡**Note:** Les valeurs `<RAMDOM_STRING>`, `<RANDOM_SECURE_LONG_STRING>` et `<MONGO_DB_CONNECTION_STRING>` sont des espaces réservés. Vous devez les remplacer par vos propres valeurs avant de déployer ou d'exécuter le backend.
- Sur les systèmes Unix, vous pouvez générer des chaînes aléatoires sécurisées pour ces clés en utilisant `openssl rand -hex 32` pour `JWT_SECRET_KEY` et `openssl rand -hex 64` pour `JWT_REFRESH_SECRET_KEY` dans votre terminal.  
- Sur Windows, vous pouvez utiliser d'autres méthodes pour générer des chaînes sécurisées.

## Démarrage du serveur

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Installez les dépendances nécessaires avec `pipenv install -r requirements.txt`. Cette étape n'est nécessaire que lors de la première installation ou lorsque de nouvelles dépendances sont ajoutées.
3. Lancez le serveur avec `uvicorn app.main:app --reload`.
   - L'API sera disponible à [http://127.0.0.1:8000](http://127.0.0.1:8000).
   - Une documentation automatique de l'API sera disponible à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) ou [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

> Pour quitter l'environnement virtuel, utilisez la commande `exit`.

## Initialisation de la base de données

Pour générer des données servant à peupler la base de données, nous utilisons les scripts définis dans le dossier `/utils`, tel que `generate_all.py`. Voici les étapes à suivre:

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Exécutez le script avec `py -m utils.generate_all`.

> Vous pouvez ajuster le nombre d'utilisateurs créés en modifiant cette ligne dans le script `generate_all.py`: `user_usernames = await create_users(27)`.  
> Par défaut, les données seront générées dans `MONGO_DB_NAME = settings.MONGO_DB_NAME + "test"`, mais vous pouvez les diriger vers votre base de données principale en modifiant le script `MONGO_DB_NAME = settings.MONGO_DB_NAME`.

## Exécuter les scripts de recommendation

Pour exécuter les scripts de recommendation qui se trouvent dans le dossier ``/recommender_systems/routines`` tel que ``clustering``, voici les étapes à suivre:

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Dépendement de vos besoins,
   - Exécutez ``py -m recommender_systems.main`` pour exécuter tous les scripts.
   - Exécutez ``py -m recommender_systems.main clustering`` pour exécuter un script en particulier.

Les noms à fournir en paramètre pour exécuter chaque script peuvent être trouvé dans le fichier ``recommender_systems/main.py``.

## Exécuter les tests
### Tests du backend
Pour exécuter les tests du *Backend*, il est nécessaire d'avoir des données générées par `generate_all.py`. Voici les étapes à suivre:

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Exécutez les tests avec `pytest`.

### Tests des scripts de recommendation
Pour exécuter les tests des *algorithmes de recommendation*, il n'est pas nécéssaire d'avoir généré  des données au préalable. Voici les
étapes à suivre:

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Exécutez les tests avec `py -m recommender_systems.tests.main`.

Pour exécuter les tests pour un seule script, l'étape 1. est la même mais l'étape 2. devient :

2. Exécutez les tests avec `py -m unittest recommender_systems.tests.test_*`. Remplacer `*` par le nom du fichier à exécuter.

# Déploiement et Hébergement

Notre backend est actuellement hébergé sur [Render](https://render.com), une plateforme gratuite idéale pour les projets en développement et en phase de test.  
Nous utilisons spécifiquement la branche `preview` sur Render pour tester les nouvelles fonctionnalités et mises à jour avant leur déploiement. 
Render héberge à la fois notre [service web (API backend)](#service-web-api) et notre [application web (frontend)](#application-web). Les configurations de ces deux éléments sont décrites ci-dessous.


> Puisque nous utilisons la version gratuite de Render, le serveur passe en mode veille après une période d'inactivité.  
Pour palier à ce cette contrainte, nous utilisons un service de [cron job externe](https://v4szkwlx.status.cron-job.org) pour envoyer une requête (**ping**) à notre API ([https://cafesansfil-api.onrender.com/api/health](https://cafesansfil-api.onrender.com/api/health)) toutes les 10 minutes pour garder l'instance active. Cette stratégie nous permet de bénéficier des 750 heures gratuites par mois offertes par Render👍.

## Service web (API)

1. **Déploiement de l'API** :
   - Sélectionnez 'Web Service' sur Render et choisissez le répertoire `/back`.
   - Utilisez la branche `preview` pour le déploiement.

2. **Commandes de Construction et de Lancement** :
   - Build Command : `pip install --upgrade pip && pip install -r requirements.txt`.
   - Start Command : `uvicorn app.main:app --host 0.0.0.0 --port 10000`.

3. **Configuration des Variables d'Environnement** :
   - Définissez les variables suivantes dans les paramètres de votre service Render :
     ```ini
     JWT_SECRET_KEY=<RANDOM_STRING>
     JWT_REFRESH_SECRET_KEY=<RANDOM_SECURE_LONG_STRING>
     BACKEND_CORS_ORIGINS=<BACKEND_CORS_ORIGINS>
     BASE_URL=<BASE_URL>
     MONGO_CONNECTION_STRING=<MONGO_DB_CONNECTION_STRING>
     MONGO_DB_NAME="cafesansfil"
     ```

## Application web

1. **Déploiement du Frontend** :
   - Sélectionnez 'Static Site' sur Render et choisissez le répertoire `/front`.
   - Utilisez également la branche `preview` pour le déploiement.

2. **Commande de Construction** :
   - Build Command : `npm install; npm run build`.
   - Publish directory : `dist`.

3. **Configuration des Redirections** :
   - Ajoutez une règle de réécriture :
     - Source : `/*`
     - Destination : `/index.html`
     - Action : `Rewrite`

4. **Variable d'Environnement pour le Frontend** :
   - Ajoutez cette variable dans `.env` : `VITE_API_ENDPOINT=https://cafesansfil-api.onrender.com` (Example).
