# 📋 Exigences

> Livrable: Exigences  
> Dernière modification: 2023-12-03

Ce document présente la liste des exigences du projet.

## Exigences fonctionnelles
> **Niveau d'accès**:  
> Chaque niveau d'accès supérieur inclut les fonctionnalités des niveaux inférieurs. 🟠 < 🔵 < 🟢 < 🔴  
> 🟠 Pour le grand public  
> 🔵 Pour les membres de l'UdeM    
> 🟢 Pour les bénévoles  
> 🔴 Pour les responsables d'un café  
<br>

### Fonctionnalités Globales 🟠

- [x] Recherche de café
  - Afficher la liste des cafés (nom, ouvert/fermé)
  - Filtrer la liste des cafés (ouvert/fermé, mode de paiement)
  - Chercher un café par nom

- [x] Café et menu
  - Afficher les informations d'un café
  - Accéder au menu d'un café
  - Afficher le détail d'un item du menu

### Fonctionnalités Clients 🔵

- [x] Authentification et profil
  - Créer un compte (nécessite un matricule et une adresse courriel de l'UdeM)
  - Se connecter (avec matricule ou adresse courriel)
  - Modifier mon profil

- [x] Passer une commande (pour ramassage)
  - Réserver un item pour ramassage (délai de 1 heure)
  - Voir l'historique des commandes

### Fonctionnalités de Staff 🟢

- [x]  Traitement des commandes
  - Afficher les commandes à traiter
  - Modifier le statut d'une commande (Placée, Prêt, Complétée, Annulée)

- [x]  Gestion du menu
  - Ajouter, modifier ou supprimer un élément du menu

### Fonctionnalités Administratives 🔴

- [x] Gestion du café
  - Modifier les informations de base d'un café
  - Créer une annonce

- [x] Gestion des bénévoles
  - Ajouter, modifier ou supprimer un staff

- [x] Rapports de ventes
  - Générer des rapports sur les ventes (journalières, hebdomadaires, mensuelles)
  - Afficher les items les plus et les moins vendus

<br>

## Exigences non fonctionnelles

**Performance**:  
L'application web doit être réactive et l'API doit répondre rapidement.

**Sécurité**:  
Les données des utilisateurs doivent être stockées en toute sécurité. L'application doit également empêcher tout accès non autorisé et protéger contre d'éventuelles vulnérabilités.

**Scalabilité**:  
Bien que l'application soit initialement destinée à l'UdeM, elle doit être conçue de manière à pouvoir gérer une augmentation du nombre d'utilisateurs.

**Disponibilité**:  
L'application doit être disponible aussi souvent que possible, avec un minimum de temps d'arrêt.

**Accessibilité**:  
L'application doit être utilisable par le plus grand nombre, y compris les personnes ayant des handicaps. Cela pourrait impliquer des ajustements pour les lecteurs d'écran ou des options pour augmenter la taille du texte, par exemple.

**Utilisabilité**:  
L'interface doit être intuitive, facile à utiliser, esthétiquement plaisante, et adaptée aux différents formats d'écrans, notamment les tablettes et les smartphones.

**Compatibilité**:  
L'application web doit être compatible avec différents navigateurs. Elle doit également être prête à supporter du multilingue à l'avenir.


**Extensibilité**:  
Il doit être facile d'ajouter de nouvelles fonctionnalités ou d'améliorer les fonctionnalités existantes à l'avenir.


**Maintenabilité**:  
Le code de l'application doit être bien documenté, structuré, et facile à maintenir. Il doit être conçu en utilisant des technologies largement reconnues, afin que d'autres développeurs puissent facilement reprendre le projet dans le futur.

**Résilience**:  
L'application doit être capable de gérer et de récupérer des erreurs.

