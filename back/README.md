# 🗄️ Back-end de Café sans-fil
  
Pour la gestion de nos données, nous utilisons MongoDB Atlas, la base de données cloud de MongoDB. Nous avons opté pour ce service en raison de son offre gratuite qui est parfaitement adaptée à nos besoins.  
  
## Prérequis

- Assurez-vous d'avoir installé Python 3.11. (Ou sinon [Creating a Pipfile for multiple versions of Python](https://dev.to/tomoyukiaota/creating-a-pipfile-for-multiple-versions-of-python-9f2))
- Si vous n'avez pas `pipenv`, installez-le avec `pip install pipenv`.
- Assurez-vous que MongoDB est installé sur votre système.

### Configuration du fichier .env

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

# 📅 Avancée du développement

## Décembre 2023

### 2023-12-03
- Mise à jour de la documentation de l'API et Back-end.

### 2023-12-02
- Mise à jour de la documentation de l'API.

## Novembre 2023

### 2023-11-30
- Mise à jour des tests pour Staff.

### 2023-11-29
- Augmentation du limitation des caractères pour `image_url` et `faculty`

### 2023-11-28
- Autorisation pour les bénévoles de mettre à jour le menu, ajustement des types de rapports.
- Ajout d'un Scheduler pour la mise à jour du statut des commandes.
- Ajout des routes et des tests de l'API pour Staff.

### 2023-11-27
- Ajout de la route pour obtenir le rapport de ventes.
- Ajout de noms et d'images dans les commandes.
- Ajout de la route Delete User.
- Ajout de `order_number`, simplification des mots de passe, et direction du sort.

### 2023-11-23
- Mise à jour de `matricule`, toujours afficher `additional_info`.

### 2023-11-22
- Téléchargement d'images sur Cloudflare CDN.
- Correction de `is_open` HH:mm et randomisation de `in_stock`.
- Changer les mots de passe des utilisateurs à `Cafepass1`.

### 2023-11-21
- Correction list order pour User/Cafe.
- Génération d'adresses e-mail avec le domaine `@umontreal.ca`.
- Désactivation de l'e-mail en raison du blocage SMTP par Render.
- Ajout de `MAIL_FROM_NAME` dans `.env`, retour en arrière pour inclure les informations d'identification.
- Ajout de listes d'origines et inclusion des informations d'identification CORS.

### 2023-11-20
- Correction des schémas.
- Refactorisation des routes pour utiliser les slugs + documentation.
- Ajout de davantage d'autorisations, ajout de la requête limite.

### 2023-11-19
- Ajout des tentatives de connexion échouées et du verrouillage.
- Ajout de mail pour l'inscription et la réinitialisation du mot de passe + documentation.
- Mise à jour : Force du mot de passe, limites de caractères, documentation.

### 2023-11-18
- Refactorisation de `is_available` en `in_stock`.
- Ajout de `status_message` dans Cafe.
- Ajout d'images de café.
- Ajout d'un route Health Check
- Ajout de workflows de test et de déploiement.

### 2023-11-17
- Résolution de davantage de dépréciations Pydantic + photos.
- Ajout de tests : auth, cafe, order, user.

### 2023-11-16
-  Résolution des dépréciations Pydantic.

### 2023-11-15
- Mise à jour majeure de la base de données : cafe, order, user.

### 2023-11-14
- Ajout de scripts de génération de données en masse.

### 2023-11-13
- Mise à jour de la recherche dynamique et du sort.
- Ajout de paramètres de requête dynamiques dans les routes de commande/utilisateur.
- Ajout de support pour les paramètres de requête dynamiques dans les routes de café.
- Mise à jour de la gestion des erreurs dans les routes de café et de commande.

### 2023-11-02
- Aperçu du projet sur la branche `preview` avec Render.

## Octobre 2023

### 2023-10-30
- Migration vers Python 3.11.
- Mise à jour des imports et des dépendances.

### 2023-10-24
- Mise à jour des schémas pour la validation des requêtes et des réponses.
- Ajout des routes d'authentification et de vérifications d'autorisation pour les rôles.

### 2023-10-21
- Amélioration de la recherche avec l'inclusion de descriptions, facultés, localisations, et filtres supplémentaires.
- Ajout de la récupération et du filtrage des commandes pour les utilisateurs et les cafés.

### 2023-10-20
- Refactorisation majeure de la structure Backend et de l'API.
- Connexion à MongoDB Atlas et population avec des données initiales.
- Ajout d'une fonctionnalité de recherche unifiée pour les cafés et les éléments de menu.
- Documentation et ajout de docstrings aux modules backend.

### 2023-10-04
- Création de `models.py` avec les premiers modèles de données.
- Création de premières routes test, testables avec Postman.

## Septembre 2023

### 2023-09-29
- Initialisation du projet avec FastAPI et création d'un environnement virtuel.
- Ajout des dépendances dans `requirements.txt`.
- Installation d'Uvicorn pour le serveur de production.
- Création de `main.py` avec le code initial de l'API.

# 📚 Ressources

- [Documentation | FastAPI](https://fastapi.tiangolo.com/learn/)
- [Documentation | Pydantic](https://docs.pydantic.dev/dev/blog/pydantic-v2-final/)
- [Documentation | Beanie](https://beanie-odm.dev/api-documentation/query/)
- [YouTube | FARM Stack Course - FastAPI, React, MongoDB](https://www.youtube.com/watch?v=OzUzrs8uJl8&list=PLAt-l74BsucNBwFANkqwisPMSLE62rKG_&index=2&t=2912s&ab_channel=freeCodeCamp.org)
- [YouTube | The ultimate FARM stack Todo app with JWT PART I - FastAPI + MongoDB | abdadeel](https://www.youtube.com/watch?v=G8MsHbCzyZ4&ab_channel=ABDLogs)
- [YouTube | Python API Development With FastAPI - Comprehensive Course for Beginners P-5 Password reset](https://www.youtube.com/watch?v=Y7FCJF48Obk&list=PLU7aW4OZeUzxL1wZVOS31LfbB1VNL3MeX&index=7&ab_channel=CodeWithPrince)
- [YouTube (For Mac) | command not found: pipenv Resolved](https://www.youtube.com/watch?v=Bzn_MZ0tNXU&ab_channel=SpecialCoder)
- [Article | Creating a Pipfile for multiple versions of Python](https://dev.to/tomoyukiaota/creating-a-pipfile-for-multiple-versions-of-python-9f2)
- [Render | Redirects and Rewrites](https://render.com/docs/redirects-rewrites)
- [Render | Spin-down behavior of free instance types](https://community.render.com/t/requests-to-back-end-take-long/10059)
- [Render | Cron Job fix for Spin-down](https://stackoverflow.com/questions/75340700/prevent-render-server-from-sleeping)
- [Render | Mail server on render.com doesn't permit SMTP](https://community.render.com/t/mail-server-on-render-com/10529)
