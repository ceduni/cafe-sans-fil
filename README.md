<br/>
<br/>
<p align="center">
  <a href="https://cafesansfil.onrender.com/">
    <img src="front/public/logo.png" width="300">
  </a>
</p>
<br/>

# Café sans-fil

Café sans-fil est un projet pilote visant à améliorer le service des cafés étudiants de l'UdeM.  
Les cafés étudiants donnent accès à un espace de socialisation et de la nourriture à prix abordable, enrichissant la vie de campus des étudiants. Toutefois, l'infrastructure actuelle ne facilite pas l'accès à l'information et alourdit la gestion des cafés.  
Nous proposons une plateforme commune facilitant la gestion des cafés, leur découverte, la communication de leurs produits et la prise de commande.

## 📋 Fonctionnalités

### Pour le grand public

- [x] **Recherche de café**
  - [x] Afficher la liste des cafés
  - [x] Filtrer la liste des cafés
  - [x] Chercher un café par nom
  - [ ] Chercher un café par item
  - [ ] Chercher un café par tag
  - [x] Afficher les informations d'un café
- [x] **Café: Menu**
  - [x] Accéder au menu d'un café
  - [x] Afficher le détail d'un item du menu
- [ ] **Café: Évènements**

### Pour les membres

- [x] **Authentification et profil**
  - [x] Créer un compte
  - [x] Modifier mon profil
- [x] **Passer une commande (pour ramassage)**
  - [x] Réserver un item
  - [x] Voir l'historique de mes commandes

### Pour les bénévoles et responsables d'un café

- [ ] **Gestion du café**
  - [x] Modifier les informations de base d'un café
  - [x] Créer une annonce
  - [ ] Personnalisation de la page du café
- [ ] **Gestion du menu**
  - [x] Ajouter, modifier ou supprimer un item
  - [ ] Modification en lot
  - [ ] Importer son menu
- [ ] **Gestion des bénévoles**
  - [x] Ajouter, modifier ou supprimer un staff
  - [ ] Gestion de l'horaire
- [ ] **Rapports de ventes**
  - [x] Générer des rapports sur les ventes journalières, hebdomadaires, et mensuelles
  - [x] Afficher les items les plus vendus et les moins vendus

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

La documentation officielle du projet se trouve dans le [wiki](https://github.com/ceduni/cafe-sans-fil/wiki).  
Pour faciliter la recherche, voilà quelques **liens rapides**:  
🔗 [Spécifications du projet](https://github.com/ceduni/cafe-sans-fil/wiki/Exigences)  
🔗 [Documentation de l'API](https://cafesansfil-api.onrender.com/redoc)  
🔗 [Documentation de la BD](https://github.com/ceduni/cafe-sans-fil/wiki/API-et-Base-de-donn%C3%A9es)

<!-- 🔗 [Guide d'utilisation](https://github.com/ceduni/cafe-sans-fil/wiki/Base-de-donn%C3%A9es-(BD))  -->

# 🗂️ Organisation

Les dossiers du répertoire sont organisés comme suit:

- `\back`: contient le code source du backend composé de l'API et de la base de données
- `\front`: contient le code source de l'application web
- `\prototype`: contient les prototypes de la nouvelle version de l'application web
- `\docs`: contient le site web du projet

# 🌟 Contribution

Si vous êtes intéressé à participer au projet, veuillez prendre contact avec [Louis-Edouard LAFONTANT](mailto:louis.edouard.lafontant@umontreal.ca).

## Contributeurs

- Louis-Edouard LAFONTANT [@lelafontant](https://github.com/lelafontant)
- Axel ZAREB [@axeelz](https://github.com/axeelz)
- Southidej OUDANONH [@GokaGokai](https://github.com/GokaGokai)
- Flory JEAN-BAPTISTE [@FloryJB](https://github.com/FloryJB)
