# Café sans-fil: Site web 🚀

Le site est développé avec le framework [**Astro**](https://astro.build/).

## Structure du projet

Les fichiers sont organisés suivant la structure suivante:

```ada
/ -- Racine du projet (/docs)
├── public/ -- Ressources statiques qui n’ont pas à être traitées (fonts, icons, etc.)
│   └── favicon.ico
├── src/ -- Code source du site
│   ├── components/ -- Code réutilisable pour les pages
│   │   └── Card.astro
│   ├── data/ -- Données du site
│   │   └── contributors.json
│   ├── layouts/ -- Composants de mise en page
│   │   └── Layout.astro
│   └── pages/ -- Pages du site
│       └── index.astro
│   └── styles/ --  Feuilles de style
│       └── base.css
│       └── normalize.css
└── astro.config.mjs -- Configuration d’Astro
└── package.json -- Manifeste du projet
```

Astro cherche les fichiers `.astro` ou `.md` dans le dossier `src/pages/`. 
Chaque page est exposée comme une route basée sur le nom du fichier.

## Installation

> Prérequis: [NodeJS](http://nodejs.org/)

Utilisez les commandes suivantes à partir du dossier `/docs`.

| Commande                  | Action                                             |
| :------------------------ | :------------------------------------------------- |
| `npm install`             | Installez les dépendences du site                  |
| `npm run dev`             | Démarrez le site localement à `localhost:4321`     |
| `npm run build`           | Compilez le site pour la production dans `./dist/` |
| `npm run preview`         | Prévisualisez la compilation, avant le déploiement |
| `npm run astro -- --help` | Obtenir de l'aide avec Astro CLI                   |
<!-- | `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` | -->
