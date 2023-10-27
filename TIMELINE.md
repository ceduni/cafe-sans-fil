# 📅 Suivi

<!-- ## Semaine 15 (2023-12-11) -->

<!-- ## Semaine 14 (2023-12-04) -->

<!-- ## Semaine 13 (2023-11-27) -->

<!-- ## Semaine 12 (2023-11-20) -->

<!-- ## Semaine 11 (2023-11-13) -->

<!-- ## Semaine 10 (2023-11-06) -->

<!-- ## Semaine 9 (2023-10-30) -->

## Semaine 8 (2023-10-23)

- **Création routes API** : Ajout de l'authentification et des authorisations pour les routes de l'API.
- **Front-end** : Avancements sur le front, création de contextes d'authentification, création UI de l'appli, création logique pour fetch l'API.
- **Connexion avec l'API** : Connexion avec l'API pour récupérer la liste des cafés et les infos sur un café.

### Résumé des discussions

- **Modération** : Comment gérer l'ajout d'un café et vérifier qui est vraiment admin? => Manuellement
- **Authentification** : Username ? => Non seulement email et matricule à l'inscription
- **Recherche** : Discussions sur la recherche, notamment sur la possibilité de rechercher par tags, et sur quelles propriétés des cafés on peut rechercher (ne pas rechercher trop large, faire en sorte que le mot commence par la query?).
- **Filtres** : Discussions sur les filtres, notamment sur la possibilité de filtrer les cafés par pavillon.
- **API** : Discussions sur l'API, notamment sur la structure de "additional_info_cafe" qui incluerait un type de message et une date de début et de fin.
- **Items du menu** : Discussions sur les items du menu, notamment sur des variations d'items (ex: un café peut avoir plusieurs tailles de café).
- **Design** : Discussions sur le design, notamment la bannière qui indique si on est admin ou bénévole d'un café, et les actions asociées. Discussions sur à quoi va ressembler d'édition d'un café en tant qu'admin.
- **Accès à la BD** : Discussions sur l'accès à la BD, installation du GUI MongoDB Compass.
- **Autre** : Switch vers la fonctionnalité Wiki sur GitHub?

## Semaine 7 (2023-10-16)

> Semaine de relâche, pas de réunion

**Avancement du front-end et de l'API**

## Semaine 6 (2023-10-09)

- **Modifications du schéma** : Modifications du schéma de la base de données pour mieux correspondre aux besoins après nos discussions de la semaine dernière.
- **Début du front-end** : Début du développement du front-end.

### Résumé des discussions

- **Design** : Discussions sur le design de l'application, les couleurs, le logo. **On doit faire une version finale du logo avec éventuellement une version réduite pour les petits formats.**
- **Concept de la page d'accueil** : Discussions sur le concept de la page d'accueil, la recherche intégrée, et notamment sur la possibilité de mettre en avant les cafés les plus proches de l'utilisateur.
  - **Décision** : On ne va pas inclure de système de localisation pour l'instant, car il faudrait que les gens acceptent de partager leur localisation, et cela pourrait être un frein pour certains utilisateurs. De plus, tout est dans le campus, donc les distances sont raisonnables.
- **Discussions sur le système de commandes** : Discussions sur le système de commandes, notamment sur la possibilité de commander des items de plusieurs cafés en même temps.
  - **Décision** : On va permettre aux utilisateurs de mettre dans leur panier des items de plusieurs cafés en même temps, puis cela créera une commande par café. Cela sera plus simple pour les utilisateurs et les cafés, et cela permettra de ne pas avoir à gérer des commandes avec des items de plusieurs cafés.

## Semaine 5 (2023-10-02)

- **Définition des modèles** : Définition des modèles de données pour la base de données (schéma).
- **Définition des routes** : Définition des premières routes de l'API, et tests avec Postman.
- **Organisation des tâches** : Création d'un GitHub Project pour organiser les tâches à faire, avec issues et milestones.

### Tâches à faire

- [x] Review tout ce qu'on a fait, valider ou non les routes et le schéma de BD

## Semaine 4 (2023-09-25)

- **Révision des flux réalisés** : Révision des flux réalisés et des exigences associées.
- **Documentation** : Ajustements et complétion de la documentation (wiki), ajout des risques.
- **Architecture** : Discussions sur l'architecture de l'application et les possibles contraintes qui pourraient arriver.
- **Initialisation de l'API** : Initialisation d'un dossier API avec FastAPI.

### Tâches à faire

- [x] Ajouter des risques dans la documentation
- [x] Définir si on utilise MongoDB ou PostgreSQL
- [x] Utiliser un outil simple pour les graphiques (notamment timeline), voir draw.io
- [x] Initialiser un dossier API avec FastAPI
- [x] Ajouter la page de point de départ dans les flux

## Semaine 3 (2023-09-18)

- **Définition des exigences** : Définition des exigences principales et secondaires.
- **Définition des flux** : Définition des flux pour les exigences principales, avec leur output et input.
- **Documentation** : Rédaction de la documentation (wiki) pour les flux et les exigences.

### Tâches à faire

- [x] Réaliser le document exigences
- [x] Réaliser les flux

## Semaine 2 (2023-09-11)

### Objectifs de la deuxième semaine

- **Débrief des besoins des cafés** : Récapitulatif des exigences et des fonctionnalités voulues par les cafés (notamment Tore et Fraction).
- **Discussion sur les technologies** : Évaluation des technologies disponibles et sélection des outils à utiliser pour le projet.
- **Définition des prochaines étapes** : Planification des prochaines étapes et des tâches à accomplir, notamment prendre chaque éxigence pour la transformer en un flux, faire des mini maquettes, etc.

### Tâches éffectuées

- Regroupement des informations utiles pour notre BDD sur tous les cafés dans un fichier JSON. (Voir [data/cafes.json](data/cafes.json))
- Initialisation du front React avec Vite. (Dans le dossier [front](front/))

## Semaine 1 (2023-09-04)

### Objectifs de la première semaine

- **Lancement du projet** : Réunion initiale pour démarrer les travaux.
- **Planification globale** : Définition de la roadmap et des étapes clés.
- **Définition des exigences** : Précision des fonctionnalités et des besoins pour l'application.
- **Communication avec les cafés** : Prise de contact avec le responsable du Café Tore et Fraction.

### Vue d'ensemble du projet

![Plan du Projet](https://cdn.discordapp.com/attachments/841456989443325973/1149925649943887943/cafe_sans_fils_rounded_updated_v2.png)

La durée totale du projet est estimée à 13 semaines. Il est catégorisé en trois sections principales : **la base de données**, **l'API** et **l'interface Web**.

### Phases clés

- **Semaines 1 à 2** : Mise en place et définition des exigences.
- **Semaines 2 à 3** : Sélection des technologies et mise en place de l'architecture des données.
- **Semaines 3 à 5** : Élaboration de l'API et de la base de données.
- **Semaines 5 à 13** : Développement et intégration des fonctionnalités principales.
- **Semaine 13** : Phase finale avec déploiement et réalisation des tests utilisateurs.

### Exigences du projet

- **Localisation des cafés** | 🔵 _Consommateur_  
  Lister les cafés basés sur leur localisation. Offrir une fonction de recherche où les utilisateurs peuvent formuler des requêtes spécifiques en utilisant des étiquettes ou des "tags" associés aux items du menu (par exemple, un tag "jus de fruits"). Incorporer l'utilisation d'une map pour une visualisation facile des emplacements des cafés et fournir des détails sur les moyens de paiement disponibles.

- **Lister les menus** | 🟠 _Public_  
  Afficher les différents items offerts par les cafés, incluant les prix, les descriptions et éventuellement des images. Permettre aux utilisateurs de parcourir les offres avant de faire une sélection.

- **Fiche de présentation d'un café** | 🟠 _Public_  
  Affichage des détails tels que photo, horaires, coordonnées, et autres informations pertinentes.

- **Identification de l'étudiant & création de compte** | 🔵 _Consommateur_  
  Mettre en œuvre un mécanisme d'authentification, utiliser un QR code, et s'intégrer avec le service UdeM.

- **Gestion du menu pour un café spécifique** | 🟢 _Bénévole_, 🔴 _Admin_  
  Ajouter, modifier, supprimer du contenu.  
  _Note_: Investiguer la structure des bénévoles au sein d'un café et définir leurs rôles.

- **Gestion de la liste des bénévoles** | 🔴 _Admin_  
  Offre aux administrateurs la capacité de gérer les bénévoles associés à un café. Cela inclut l'ajout, la modification, et la suppression de bénévoles, ainsi que la gestion de leurs rôles et responsabilités.

- **Prise de commande** | 🔵 _Consommateur_, 🟢 _Bénévole_  
  Permet aux consommateurs de sélectionner et commander des items du menu. Les bénévoles reçoivent et traitent ces commandes pour préparation.

- **Paiement en ligne** | 🔵 _Consommateur_, 🔴 _Admin_  
  Intégrer des contraintes comme un montant minimum et des frais.

- **Rapports et statistiques** | 🟢 _Bénévole_, 🔴 _Admin_  
  Générer des rapports de vente, statistiques et autres informations pertinentes.

- **Système de récompenses/Gamification** | 🔵 _Consommateur_, 🔴 _Admin_  
  Introduit un mécanisme incitatif pour encourager les consommateurs à passer des commandes ou à participer à certaines activités. Les récompenses peuvent être sous forme de points, de remises ou d'autres avantages.

- **Canal de communication** | 🔵 _Consommateur_, 🟢 _Bénévole_  
  Offrir un moyen pour les recommandations, sondages et autres formes de communication.
