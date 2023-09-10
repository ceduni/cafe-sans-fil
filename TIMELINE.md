# Échéancier

<!-- ## Semaine 15 (2023-12-11) -->

<!-- ## Semaine 14 (2023-12-04) -->

<!-- ## Semaine 13 (2023-11-27) -->

<!-- ## Semaine 12 (2023-11-20) -->

<!-- ## Semaine 11 (2023-11-13) -->

<!-- ## Semaine 10 (2023-11-06) -->

<!-- ## Semaine 9 (2023-10-30) -->

<!-- ## Semaine 8 (2023-10-23) -->

<!-- ## Semaine 7 (2023-10-16) -->

<!-- ## Semaine 6 (2023-10-09) -->

<!-- ## Semaine 5 (2023-10-02) -->

<!-- ## Semaine 4 (2023-09-25) -->

<!-- ## Semaine 3 (2023-09-18) -->

<!-- ## Semaine 2 (2023-09-11) -->

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

- **Localisation des cafés** | 🔵 *Consommateur*  
  Lister les cafés basés sur leur localisation. Offrir une fonction de recherche où les utilisateurs peuvent formuler des requêtes spécifiques en utilisant des étiquettes ou des "tags" associés aux items du menu (par exemple, un tag "jus de fruits"). Incorporer l'utilisation d'une map pour une visualisation facile des emplacements des cafés et fournir des détails sur les moyens de paiement disponibles.

- **Lister les menus** | 🟠 *Public*  
  Afficher les différents items offerts par les cafés, incluant les prix, les descriptions et éventuellement des images. Permettre aux utilisateurs de parcourir les offres avant de faire une sélection.

- **Fiche de présentation d'un café** | 🟠 *Public*  
  Affichage des détails tels que photo, horaires, coordonnées, et autres informations pertinentes.

- **Identification de l'étudiant & création de compte** | 🔵 *Consommateur*  
  Mettre en œuvre un mécanisme d'authentification, utiliser un QR code, et s'intégrer avec le service UdeM.

- **Gestion du menu pour un café spécifique** | 🟢 *Bénévole*, 🔴 *Admin*  
  Ajouter, modifier, supprimer du contenu.  
  _Note_: Investiguer la structure des bénévoles au sein d'un café et définir leurs rôles.

- **Gestion de la liste des bénévoles** | 🔴 *Admin*  
  Offre aux administrateurs la capacité de gérer les bénévoles associés à un café. Cela inclut l'ajout, la modification, et la suppression de bénévoles, ainsi que la gestion de leurs rôles et responsabilités.

- **Prise de commande** | 🔵 *Consommateur*, 🟢 *Bénévole*  
  Permet aux consommateurs de sélectionner et commander des items du menu. Les bénévoles reçoivent et traitent ces commandes pour préparation.

- **Paiement en ligne** | 🔵 *Consommateur*, 🔴 *Admin*  
  Intégrer des contraintes comme un montant minimum et des frais.

- **Rapports et statistiques** | 🟢 *Bénévole*, 🔴 *Admin*  
  Générer des rapports de vente, statistiques et autres informations pertinentes.

- **Système de récompenses/Gamification** | 🔵 *Consommateur*, 🔴 *Admin*  
  Introduit un mécanisme incitatif pour encourager les consommateurs à passer des commandes ou à participer à certaines activités. Les récompenses peuvent être sous forme de points, de remises ou d'autres avantages.

- **Canal de communication** | 🔵 *Consommateur*, 🟢 *Bénévole*  
  Offrir un moyen pour les recommandations, sondages et autres formes de communication.
