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
