# Front-end de Café sans-fil

## Développement

- On utilise React et Vite pour le développement
- On utilise [Tailwind CSS](https://tailwindcss.com/) pour le style
- Afin de ne pas perdre de temps à créer des composants, on utilise [Tailwind UI](https://tailwindui.com/) pour certains composants
- On utilise également [shadcn ui](https://ui.shadcn.com/) pour certains composants (pas de dépendance, juste du copier-coller)

## Installation

- Avoir installé Node.js
- Avoir installé npm
- Exectuer `npm install` pour installer les dépendances
- Exectuer `npm run dev` pour lancer le serveur de développement
- Le front sera disponible à l'adresse indiquée dans le terminal (par défaut [http://localhost:5173](http://localhost:5173))

## Avancée du développement

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
