# 🗄️ Back-end de Café sans-fil
  
Pour la gestion de nos données, nous utilisons MongoDB Atlas, la base de données cloud de MongoDB. Nous avons opté pour ce service en raison de son offre gratuite qui est parfaitement adaptée à nos besoins.  
  
Notre documentation de l'API back-end est disponible via Swagger UI et ReDoc aux URL suivantes :  
  
- Swagger UI : [cafesansfil-api.onrender.com/docs](https://cafesansfil-api.onrender.com/docs)  
- ReDoc : [cafesansfil-api.onrender.com/redoc](https://cafesansfil-api.onrender.com/redoc)  
  

## Prérequis

- Assurez-vous d'avoir installé Python 3.11. (Ou sinon [Creating a Pipfile for multiple versions of Python](https://dev.to/tomoyukiaota/creating-a-pipfile-for-multiple-versions-of-python-9f2))
- Si vous n'avez pas `pipenv`, installez-le avec `pip install pipenv`.

## Configuration de MongoDB

Pour configurer MongoDB :

1. Assurez-vous que MongoDB est installé sur votre système.
2. Démarrez le serveur MongoDB.
3. Créez une nouvelle base de données nommée `"cafesansfil"` (ou le nom que vous avez défini après dans `MONGO_DB_NAME`).
4. (Facultatif) Utilisez un outil comme MongoDB Compass pour gérer et visualiser vos données plus facilement.

## Configuration du fichier .env

Pour configurer le fichier .env dans le backend, créez un fichier nommé `.env` dans `/back/app`. Ajoutez ce qui suit dans le fichier `.env` :

```
JWT_SECRET_KEY=<RAMDOM_STRING>
JWT_REFRESH_SECRET_KEY=<RANDOM_SECURE_LONG_STRING>
BACKEND_CORS_ORIGINS=<BACKEND_CORS_ORIGINS> # "http://localhost:5173" <-- for local running instances
BASE_URL=<BASE_URL> # "http://localhost:8000" <-- for local running instances
MONGO_CONNECTION_STRING=<MONGO_DB_CONNECTION_STRING> # "mongodb://localhost:27017/" <-- for local running instances
MONGO_DB_NAME="cafesansfil"
```

> **Note:** Les valeurs `<RAMDOM_STRING>`, `<RANDOM_SECURE_LONG_STRING>` et `<MONGO_DB_CONNECTION_STRING>` sont des espaces réservés. Vous devez les remplacer par vos propres valeurs avant de déployer ou d'exécuter le backend. Sur les systèmes Unix, vous pouvez générer des chaînes aléatoires sécurisées pour ces clés en utilisant `openssl rand -hex 32` pour `JWT_SECRET_KEY` et `openssl rand -hex 64` pour `JWT_REFRESH_SECRET_KEY` dans votre terminal. Sur Windows, vous pouvez utiliser d'autres méthodes pour générer des chaînes sécurisées.

## Démarrage du server

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Installez les dépendances nécessaires avec `pipenv install -r requirements.txt`. Cette étape n'est nécessaire que lors de la première installation ou lorsque de nouvelles dépendances sont ajoutées.
3. Lancez le serveur avec `uvicorn app.main:app --reload`.

- L'api sera disponible à [http://127.0.0.1:8000](http://127.0.0.1:8000).
- Une documentation automatique de l'API est disponible à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) ou [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

> Pour quitter l'environnement virtuel, utilisez la commande `exit`.

## Génération de Données avec `generate_all.py` dans `utils`

Pour générer des données pour la base de données :

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Exécutez le script avec `py -m utils.generate_all`.

> Vous pouvez ajuster le nombre d'utilisateurs créés en modifiant cette ligne dans le script : `user_usernames = await create_users(27)`.

Par défaut, les données seront générées dans `MONGO_DB_NAME = settings.MONGO_DB_NAME + "test"`, mais vous pouvez les diriger vers votre base de données principale en modifiant le script `MONGO_DB_NAME = settings.MONGO_DB_NAME`.

## Run Tests

Pour exécuter les tests du back-end, il est nécessaire d'avoir des données générées par `generate_all.py` :

1. Depuis le dossier `/back`, activez l'environnement virtuel avec `pipenv shell`.
2. Exécutez les tests avec `pytest`.

<br>

# ☁️ Hosting `preview` branch sur Render

Notre application back-end est actuellement hébergée sur [Render](https://render.com), une plateforme d'hébergement gratuite et idéale pour les projets en phase de développement et de test. Sur Render, nous hébergeons spécifiquement la branche `preview`, ce qui nous permet de tester les nouvelles fonctionnalités et mises à jour avant leur déploiement. Render est utilisé pour héberger à la fois le service web (API back-end) et le site statique (front-end). Voici comment nous avons configuré chaque partie :

## Web Service pour l'API (Back-end)

1. **Déploiement de l'API** :
   - Sélectionnez 'Web Service' sur Render et choisissez le répertoire `/back`.
   - Utilisez la branche `preview` pour le déploiement.

2. **Commandes de Construction et de Lancement** :
   - Build Command : `pip install --upgrade pip && pip install -r requirements.txt`.
   - Start Command : `uvicorn app.main:app --host 0.0.0.0 --port 10000`.

3. **Configuration des Variables d'Environnement** :
   - Définissez les variables suivantes dans les paramètres de votre service Render :
     ```
     JWT_SECRET_KEY=<RANDOM_STRING>
     JWT_REFRESH_SECRET_KEY=<RANDOM_SECURE_LONG_STRING>
     BACKEND_CORS_ORIGINS=<BACKEND_CORS_ORIGINS>
     BASE_URL=<BASE_URL>
     MONGO_CONNECTION_STRING=<MONGO_DB_CONNECTION_STRING>
     MONGO_DB_NAME="cafesansfil"
     ```

## Static Site pour le Front-end

1. **Déploiement du Front-end** :
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

4. **Variable d'Environnement pour le Front-end** :
   - Ajoutez cette variable dans `.env` : `VITE_API_ENDPOINT=https://cafesansfil-api.onrender.com` (Example).

Ces configurations permettent de déployer et de gérer efficacement l'API et le front-end sur Render, en utilisant la branche `preview` pour des mises à jour continues et des tests avant la mise en production.

## Gestion du Spin-Down avec un Cron Job

Pour éviter le comportement de "spin-down" des instances gratuites sur Render, où le serveur passe en mode veille après une période d'inactivité, nous avons mis en place un mécanisme externe :

- Nous utilisons un service de cron job externe pour envoyer une requête à notre API toutes les 10 minutes. Ce service ping [https://cafesansfil-api.onrender.com/api/health](https://cafesansfil-api.onrender.com/api/health) pour garder l'instance active.
- Vous pouvez consulter l'état de notre cron job à [https://v4szkwlx.status.cron-job.org](https://v4szkwlx.status.cron-job.org).
- Cette méthode nous permet de bénéficier des 750 heures gratuites par mois offertes par Render, ce qui est suffisant pour permettre à notre API de fonctionner en continu sans interruption.

Cette stratégie assure que notre API reste accessible et réactive pour les utilisateurs, tout en maximisant les avantages des ressources gratuites fournies par Render.

<br>

# Ressources

- [Documentation | FastAPI](https://fastapi.tiangolo.com/learn/)
- [Documentation | Pydantic](https://docs.pydantic.dev/dev/blog/pydantic-v2-final/)
- [Documentation | Beanie](https://beanie-odm.dev/api-documentation/query/)
- [YouTube | FARM Stack Course - FastAPI, React, MongoDB](https://www.youtube.com/watch?v=OzUzrs8uJl8&list=PLAt-l74BsucNBwFANkqwisPMSLE62rKG_&index=2&t=2912s&ab_channel=freeCodeCamp.org)
- [YouTube | The ultimate FARM stack Todo app with JWT PART I - FastAPI + MongoDB | abdadeel](https://www.youtube.com/watch?v=G8MsHbCzyZ4&ab_channel=ABDLogs)
- [YouTube | Python API Development With FastAPI - Comprehensive Course for Beginners P-5 Password reset](https://www.youtube.com/watch?v=Y7FCJF48Obk&list=PLU7aW4OZeUzxL1wZVOS31LfbB1VNL3MeX&index=7&ab_channel=CodeWithPrince)
- [YouTube (For Mac) | command not found: pipenv Resolved](https://www.youtube.com/watch?v=Bzn_MZ0tNXU&ab_channel=SpecialCoder).
- [Article | Creating a Pipfile for multiple versions of Python](https://dev.to/tomoyukiaota/creating-a-pipfile-for-multiple-versions-of-python-9f2)
- [Render | Redirects and Rewrites](https://render.com/docs/redirects-rewrites)
- [Render | Spin-down behavior of free instance types](https://community.render.com/t/requests-to-back-end-take-long/10059)
- [Render | Cron Job fix for Spin-down](https://stackoverflow.com/questions/75340700/prevent-render-server-from-sleeping)
- [Render | Mail server on render.com doesn't permit SMTP](https://community.render.com/t/mail-server-on-render-com/10529)
