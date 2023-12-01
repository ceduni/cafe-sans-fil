<br/>
<br/>
<p align="center">
  <a href="https://cafesansfil.onrender.com/">
    <img src="/front/public/logo.png" width="300">
  </a>
</p>
<br/>

# Café sans fil

Ce projet pilote vise à améliorer le service des cafés étudiants de l'UdeM. Il consiste à développer une application web complète (backend + frontend) facilitant la recherche de cafés et produits, la prise de commandes et la gestion du menu et de l'inventaire.

L'application sera accessible à tout membre de l'UdeM (étudiant, employé, professeur, chercheur...) et offrira certains rôles assurant le bon maintien des informations présentées sur l'application.

## 📋 Fonctionnalités

### Pour le grand public

- [x] **Recherche de café**
  - [x] Afficher la liste des cafés
  - [x] Filtrer la liste des cafés
  - [x] Chercher un café par nom
- [x] **Café et menu**
  - [x] Afficher les informations d'un café
  - [x] Accéder au menu d'un café
  - [x] Afficher le détail d'un item du menu

### Pour les membres de l'UdeM

- [x] **Authentification et profil**
  - [x] Créer un compte
  - [x] Se connecter
  - [x] Modifier mon profil
- [x] **Passer une commande (pour ramassage)**
  - [x] Réserver un item
  - [x] Voir l'historique de mes commandes

### Pour les bénévoles et responsables d'un café

- [x] **Gestion du café**
  - [x] Modifier les informations de base d'un café
  - [x] Créer une annonce
- [x] **Gestion du menu**
  - [x] Ajouter, modifier ou supprimer un item
- [x] **Gestion des bénévoles**
  - [x] Ajouter, modifier ou supprimer un staff
- [x] **Rapports de ventes**
  - [x] Générer des rapports sur les ventes journalières, hebdomadaires, et mensuelles
  - [x] Afficher les items les plus vendus et les moins vendus

<!-- ## 👥 Roles

L'application offrira certains rôles donnant accès à certaines fonctionnalités.

- **Membre**: Rôle **de base** dans l'application. Avec ce rôle, un utilisateur peut accéder au menu et passer des commandes.
- **Staff**: Rôle **réservé aux bénévoles** travaillant au café, incluant toutes les actions du rôle membre. Il permet en plus de traiter les commandes, modifier le menu et gérer l'inventaire.
- **Admin**: Rôle **réservé aux responsables de la maintenance** de l'application, incluant toutes les actions du rôle membre. Il permet de faire toute opération sur la base de données. -->

## 📅 Échéancier

Le projet se découpe en plusieurs phases. La phase 1 commence à l'automne 2023 et se concentre sur le prototypage de l'application et le développement de l'API.

> **Phase 1**  
> Début: 1er septembre 2023  
> Fin: 11 décembre 2023  

Le suivi du projet est présenté dans le fichier [**TIMELINE**](TIMELINE.md).

## 🌐 Infrastructure

L'infrastructure de l'application est basée sur le **FARM stack**, comprenant FastAPI, React et MongoDB.  
Elle utilise MongoDB pour une gestion efficace des données, FastAPI pour traiter les requêtes et React pour offrir une interface utilisateur pour visualiser et interagir avec les données.

### 🗄️ Base de données

- [**MongoDB**](https://www.mongodb.com/): Base de données NoSQL orientée document.

### 🔗 API

- [**FastAPI**](https://fastapi.tiangolo.com/): Framework Python facilitant le développement d'API de style REST.

### 💻 Application web

- [**React**](https://react.dev/): Librairie JavaScript facilitant le développement d'application web en mode single-page application (SPA).
- [**Tailwind CSS**](https://tailwindcss.com/): Framework CSS open-source.

# 📘 Documentation

La documentation officielle du projet se trouve dans le [wiki](https://github.com/ceduni/udem-cafe/wiki).  
Pour faciliter la recherche, voilà quelques **liens rapides**:  
🔗 [Spécifications du projet](https://github.com/ceduni/udem-cafe/wiki/Exigences)  
🔗 [Documentation de l'API](https://github.com/ceduni/udem-cafe/wiki/API)  
🔗 [Documentation de la BD](https://github.com/ceduni/udem-cafe/wiki/Base-de-donn%C3%A9es-(BD)) 
<!-- 🔗 [Guide d'utilisation](https://github.com/ceduni/udem-cafe/wiki/Base-de-donn%C3%A9es-(BD))  -->


# 🗂️ Organisation

Les dossiers du répertoire sont organisés comme suit:

- back: contient le code source du backend composé de l'API et de la base de données
- front: contient le code source de l'application web
- wiki: contient la documentation du projet

# 🌟 Contribution

Le projet est supervisé par Louis-Edouard LAFONTANT.  
Si vous êtes intéressé à participer au projet la session prochaine (hiver 2024), contactez [Louis-Edouard LAFONTANT](mailto:louis.edouard.lafontant@umontreal.ca) d'ici le 20 décembre 2023.

## Contributeurs

- Axel ZAREB [@axeelz](https://github.com/axeelz)
- Southidej OUDANONH [@GokaGokai](https://github.com/GokaGokai)
