# Exigences

> Livrable: Exigences  
> Dernière modification: 2023-09-25

Ce document présente la liste des exigences du projet.

## Exigences fonctionnelles

Ci-dessous nous dressons la liste des fonctionnalités de l'application regroupées par niveau d'accès.

### Niveau d'accès

- 🟠 [_Public_](#fonctionnalités-publiques-🟠-public): Fonctionnalités accessibles à tout utilisateur de l'application, c.-à-d., toute personne pouvant s'y rendre
- 🔵 [_Client_](#fonctionnalités-client-🔵-client): Fonctionnalités accessibles aux clients des cafés, c.-à-d., toute personne possédant un compte à l'Université de Montréal
- 🟢 [_Bénévole_](#fonctionnalités-administratives-🟢-bénévole-🔴-admin): Fonctionnalités accessibles à tout étudiant agissant comme bénévole d'un café
- 🔴 [_Admin_](#fonctionnalités-administratives-🟢-bénévole-🔴-admin): Fonctionnalités accessibles à tout étudiant agissant comme administrateur d'un café

### Fonctionnalités globales 🟠

#### Connexion 

- Créer un compte
  - Nécessite un matricule et une adresse courriel de l'UdeM
- Se connecter
  - Avec son matricule ou son adresse courriel

### Recherche

- Chercher un café par nom ou par item
- Afficher la liste des cafés 
  - Nom du café
  - Ouvert/Fermé
  - Proximité
- Filtrer la liste des cafés
  - Ouvert/Fermé (horaires)
  - Mode de paiement
  - Type d'items du menu disponibles

#### Café et menu

- Afficher les informations d'un café
  - Nom du café
  - Description détaillée
  - Photo du café
  - Horaires d'ouverture et de fermeture
  - Moyens de paiement acceptés
- Accéder au menu d'un café
  - Lister les items du menu
  - Filtrer le menu par type d'item
  - Filtrer le menu par item disponible
- Afficher le détail d'un item du menu: 
  - nom
  - description
  - prix
  - photo
  - vegan
  - ...

### Fonctionnalités client 🔵 _Client_ 

#### Passer une commande

- Réserver un item pour ramassage dans un café (délai de 1 heure max)
  - Ajout d'articles à un panier.
  - Visualisation du total de la commande.
  - Finalisation et passation de la commande.
- Voir l'historique des commandes pour chaque membre

### Fonctionnalités administratives 🟢 _Bénévole_, 🔴 _Admin_

#### Traitement des commandes

- Afficher les commandes à traiter.
- Modifier le statut d'une commande
  - Commande complétée
  - Commande annulée

#### Café et Menu

- Ajouter, modifier ou supprimer un élément du menu
- Ajouter, modifier ou supprimer un bénévole
- Modifier le rôle d'un utilisateur

#### Rapports

- Générer des rapports sur les ventes journalières, hebdomadaires, et mensuelles.
- Afficher les items les plus vendus et les moins vendus

## Exigences non fonctionnelles

### Performance

L'application web doit être réactive et l'API doit répondre rapidement.

### Sécurité

Les données des utilisateurs doivent être stockées en toute sécurité.
L'application doit également empêcher tout accès non autorisé et protéger
contre d'éventuelles vulnérabilités.

### Scalabilité

Bien que l'application soit initialement destinée à l'UdeM, elle doit être conçue de manière à pouvoir gérer une augmentation du nombre
d'utilisateurs.

### Disponibilité

L'application doit être disponible aussi souvent que possible, avec un
minimum de temps d'arrêt.

### Accessibilité

L'application doit être utilisable par le plus grand nombre, y compris les personnes ayant des handicaps. Cela pourrait impliquer des ajustements pour les lecteurs d'écran ou des options pour augmenter la taille du texte, par exemple.

### Utilisabilité

L'interface doit être intuitive, facile à utiliser, esthétiquement plaisante, et adaptée aux différents formats d'écrans, notamment les tablettes et les smartphones.

### Compatibilité

L'application web doit être compatible avec différents navigateurs. Elle doit également supporter à la fois le français et l'anglais.

### Extensibilité

Il doit être facile d'ajouter de nouvelles fonctionnalités ou d'améliorer les fonctionnalités existantes à l'avenir.

### Maintenabilité

Le code de l'application doit être bien documenté, structuré, et facile à
maintenir. De plus, il doit être conçu en utilisant des technologies
largement reconnues, afin que d'autres développeurs, y compris les
étudiants de l'UdeM, puissent facilement reprendre et développer le projet dans le futur.

### Résilience

L'application doit être capable de gérer et de récupérer des erreurs