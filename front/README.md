# Front-end de Café sans-fil

## Développement

- On utilise React et Vite pour le développement
- On utilise [Tailwind CSS](https://tailwindcss.com/) pour le style
- Afin de ne pas perdre de temps à créer des composants, on utilise [Tailwind UI](https://tailwindui.com/) pour certains composants

## Installation

- Avoir installé Node.js
- Avoir installé npm
- Exectuer `npm install` pour installer les dépendances
- Exectuer `npm run dev` pour lancer le serveur de développement
- Le front sera disponible à l'adresse indiquée dans le terminal (par défaut [http://localhost:5173](http://localhost:5173))

### Configuration du fichier .env

- Créer un fichier `.env` à la racine du dossier front
- Ajouter la ligne `VITE_API_URL=http://127.0.0.1:8000` dans le fichier `.env`

## Structure du projet

- `src` : Dossier contenant le code source
  - `assets` : Dossier contenant les assets (icones, images, etc.)
  - `components` : Dossier contenant les composants React, ceux appartenant à une catégorie sont dans un sous-dossier, les généraux sont à la racine

## Avancée du développement

#### 2023-11-27

- POST des commandes fonctionnel
- Affichage des cafés dont on est staff sur le profil
- Possibilité de show le password sur la page de connexion
- Commencé à proprement afficher les commandes en cours d'un café
- Fix requetes API inutiles et amélioration temps chargement Orders

#### 2023-11-23

- Améliorations Navbar et hover sur les ItemCard

#### 2023-11-22

- Fix, améliorations UI et de code
- Ajout filtre commandes par statut
- Ajout options à liste commandes
- Affichage liste staff

#### 2023-11-21

- Corrections de bugs et améliorations UI
- Ajout du support des options de produits (ex: taille, sirop, etc.)
- Début support photos de profil user
- Début support des commandes côté café

#### 2023-11-16

- Corrections de bugs et améliorations UI
- Affichage réel si café ouvert ou fermé en fonction de l'heure + execution filtres sur le front

#### 2023-11-15

- Adaptation du code pour la nouvelle version de l'API et de la base de données
- Affichage des images et diverses améliorations et fix de bugs
- Générer les filtres de pavillon en fonction des pavillons existants dans la base de données
- Améliorations UI
- Afficher les bannières d'info qui si on est dans leur période d'affichage

#### 2023-11-14

- Amélioration error handling
- Optimisations panier et page item
- Optimisation de code avec fonctions utilitaires
- Début développement page de confirmation de commande

#### 2023-11-09

- Améliorations UI suivant la réunion d'équipe
- Ajout des catégories et des socials sur la page café
- Amélioration page vue produit
- Améliorations page d'accueil
- Améliorations recherche de cafés
- Filtre is_open fonctionnel
- Début de l'implémentation du panier

#### 2023-11-08

- Création de compte fonctionnelle
- Début implémentation token JWT dans requêtes API avec Axios
- Affichage des vraies infos profil utilisateur
- Ajout liste des commandes
- Mises à jour UI

#### 2023-11-06

- Début de l'implémentation de la création de compte
- Diverses optimisations dans le code et la structure de fichiers

#### 2023-11-02

- Ajout d'un Footer

#### 2023-11-01

- Ajout recherche de cafés, optimisations de code et améliorations UI

#### 2023-10-27

- Connexion login à l'API, récupération du token et stockage dans le local storage

#### 2023-10-26

- Améliorations UI liste cafés et page café et séparation du code en composants
- Ajout infos de contact et réseaux sociaux sur page café
- Ajout méthodes de paiement sur page café
- Affichage additional_info_cafe sur page café

#### 2023-10-24

- Branchement de la page de café avec l'API pour récupérer les données d'un café à partir de son ID en cliquant sur une carte d'un café

#### 2023-10-23

- Modifications mineures de design
- Maquette page ResetPassword

#### 2023-10-22

- Connexion avec l'API pour récupérer la liste des cafés, création animation de chargement

#### 2023-10-20

- Modifications design et implémentation authentification fonctionnelle (fake pour l'instant - n'importe quel email et mot de passe fonctionne)

#### 2023-10-19

- Modifications de design après discussions en équipe
- Maquette de la page d'accueil avec cartes des cafés
- Retiré page de recherche pour l'incorporer dans la page d'accueil
- Création cards cafés
- Ajout filtres sur la page d'accueil pour filtrer les cafés
- Ajout vue de bénévole / admin sur un café
- Correction de divers bugs dans le code
- Ajout de la ProductView pour afficher en détail un produit et pouvoir l'ajouter au panier
- Ajout quantité produits dans le panier
- Début création contexte d'authentification et render des composants de manière conditionnelle (navbar notamment)

#### 2023-10-09

- Création de quelques composants de base
- Début création page de profil
- Début création page de café, affichage liste staff et header de page de commande
- Début création carte affichage menu
- Création Avatar cliquable pour afficher le menu de profil et déconnexion

#### 2023-10-07

- Début de la création de la page d'accueil
- Début de la création du menu de navigation et du système de routing
- Création d'une page d'erreur
- Début de la création de la page de connexion et d'inscription
- Début de maquettes pour le panier et la page de recherche

#### 2023-09-20

- Initialisation du dossier front, setup du projet avec Vite et React

## Ressources utiles

- [Tailwind documentation](https://tailwindcss.com/docs)
- [Small and reusable Tailwind components with React - Lucky Media](https://www.luckymedia.dev/blog/small-and-reusable-tailwind-components-with-react)
- [Building reusable React components using Tailwind CSS - LogRocket Blog](https://blog.logrocket.com/building-reusable-react-components-using-tailwind-css/)
- [React Router 6: Authentication](https://www.robinwieruch.de/react-router-authentication/)
- [Complete guide to authentication with React Router v6 - LogRocket Blog](https://blog.logrocket.com/complete-guide-authentication-with-react-router-v6/)
- [Handling JWT Access and Refresh Token using Axios in React App](https://blog.theashishmaurya.me/handling-jwt-access-and-refresh-token-using-axios-in-react-app)
- [useApi React Hook | Andrew Stevens](https://andrewstevens.dev/posts/useApi-react-hook/)
