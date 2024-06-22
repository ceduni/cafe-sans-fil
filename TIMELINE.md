# 📅 Suivi

<!-- ## Semaine 15 (2024-08-09)

### Objectifs

### Réalisations

### Observations

### Ressources

## Semaine 14 (2024-08-02)

### Objectifs

### Réalisations

### Observations

### Ressources

## Semaine 13 (2024-07-26)

### Objectifs

### Réalisations

### Observations

### Ressources

## Semaine 12 (2024-07-19)

### Objectifs

### Réalisations

### Observations

### Ressources

## Semaine 11 (2024-07-12)

### Objectifs

### Réalisations

### Observations

### Ressources

## Semaine 10 (2024-07-05)

### Objectifs

### Réalisations

### Observations

### Ressources

## Semaine 9 (2024-06-28)

### Objectifs

### Réalisations

### Observations

### Ressources -->

## Semaine 8 (2024-06-21)

### Objectifs
- Créer des tests unitaires.
- Débugger le code.
- Créer une base de données pour les recommendations.
- Début du front-end.

<!--
### Réalisations

### Observations

### Ressources
-->

## Semaine 7 (2024-06-14)

### Objectifs
- Mise à jour des diagrammes.
- Mise à jour des attributs des repas et des utilisateurs pour la base de données.
- Modifier la base de données.
- Implémenter les algorithmes de recommandation.
- Créer des tests unitaires.

### Réalisations
- Mise à jour des <a href="https://cafe-sans-fil-recommendation-diagrams.netlify.app/" target="_blank">diagrammes</a>.</li>
- Implémentation des algorithmes et du robot santé.</li>
- Mise à jour des attributs des repas et des utilisateurs pour la base de données et modification de la base de données.</li>


## Semaine 6 (2024-06-07)

### Objectifs
- Mise au propre des algorithmes et écrire les pseudo code.
- Reconception d'un nouveau diagramme décrivant le fonctionant global du système.

### Réalisations
- Écriture des pseudos code des algorithmes.
- Mise en place d'une architecture pour l'implémentation.
- Création d'un diagramme présentant la pipeline du projet.

## Semaine 5 (2024-06-03)

### Objectifs
- Concevoir un algorithme pour déterminer les habitudes de consommations des étudiants en fonction de l’heure de la journée.
- Définir un schéma pour les données.

### Réalisations
- Conception d'un algorithme pour déterminer les habitudes de consommation des utilisateurs.
- Conception d'un algorithme pour attribuer un moment de la journée à un repas (à quel moment il doit être consommé).
- Première version du schéma des données définit (modification toujours en cours).

### Ressources 
- [Score santé yuka](https://help.yuka.io/l/en/article/ijzgfvi1jq)
- [Comment organiser sa journée et sa répartition calorique](https://media.dietis.fr/sante-et-alimentation/conseils-nutrition-sante/893-repartition-calorique-quotidienne.html)
- [Comprendre la densité nutritionnelle | Ethiquable](https://www.ethiquable.coop/page-guide-dachats-espace-presse/comprendre-densite-nutritionnelle#:~:text=Il%20existe%20plusieurs%20d%C3%A9finitions%20mais,%C3%A0%20son%20contenu%20en%20calories.)

## Semaine 4 (2024-05-27)

### Objectifs
- Conception d'un robot de recommandation et d'une fonction de score santé.

### Réalisations
- Ajout de la logique pour le robot de recommandation.
- Définition d'une hiérarchie des repas basé sur le niveau de transformation des aliments ainsi que le niveau de cuisson nécessaire pour consommer l'aliment.
- Définition d’une fonction score santé basé sur trois autres scores (Score basé sur la fraîcheur, Densité nutritionnelle, Score basé sur le niveau hiérarchique)

### Ressources
- [Comprendre la densité nutritionnelle | Ethiquable](https://www.ethiquable.coop/page-guide-dachats-espace-presse/comprendre-densite-nutritionnelle#:~:text=Il%20existe%20plusieurs%20d%C3%A9finitions%20mais,%C3%A0%20son%20contenu%20en%20calories.)

## Semaine 3 (2024-05-20)

### Objectifs
- Révision et amélioration de la logique du système
- Conception des diagrammes décrivant le fonctionnement du système

### Réalisations
- Ajout d'une logique pour la recommandation des cafés
- Lecture sur les algorithmes CARS ([Context Aware Recommender Systems](https://link.springer.com/chapter/10.1007/978-1-4899-7637-6_6#:~:text=In%20contrast%2C%20context%2Daware%20recommender,but%20also%20the%20context%20in)) pour la recommandation basé sur les préférences de l'utilisateur
- Définition des attributs les plus importants pour recommander un repas (Heure de la journée, Valeurs nutritives, Catégorie de repas, Fraicheur des aliments, Préférence de l'individu)
- Diagramme général présentant toute la logique du projet

### Observations
- Découverte d'autoML ([Automated Machine Learning](https://www.automl.org/automl/)): Outil permettant l'automatisation de tout le processus d'entraînement, de recherche du meilleur modèle ainsi que des meilleurs hyperparamètres.

### Ressources 
- [Context Aware Recommender Systems](https://link.springer.com/chapter/10.1007/978-1-4899-7637-6_6#:~:text=In%20contrast%2C%20context%2Daware%20recommender,but%20also%20the%20context%20in)
- [Automated Machine Learning](https://www.automl.org/automl/)

## Semaine 2 (2024-05-13)

### Objectifs
- Chercher des algorithmes de système de recommendation
- Élaborer un algorithme (pseudo code) spécifique à café sans fil

### Réalisations
- Les algorithmes suivant ont été trouvés : Content-based filtering, Collaborative filtering, knowledge-based recommender, sentiment analysis.
- Réalisation d'une première version du pseudo code pour récupérer les informations nécessaire ainsi que le prétraitement des ces données.
- Réalisation d'une première version du pseudo code d'un système hybride comprenant les algorithmes trouvés plus haut.

### Observations
- Existence d'algorithmes de recommandation utilisant la diffusion ([diffusion Modeling based Recommender Systems](https://blog.reachsumit.com/posts/2023/04/diffusion-for-recsys/)). Ces algorithmes utilisent des chaînes de Markov et sont utiles si les préférences des utilisateurs sont assez variables.<br/>
ALgorithmes très interressant mais pas très pertinent dans notre cas puisque les préférences des utilisateurs peuvent changer au début mais auront tendance à se stabiliser dans le temps.

### Ressources
- [Sentiment analysis](www.sciencedirect.com)
- [Diffusion Modeling based Recommender Systems](https://blog.reachsumit.com/posts/2023/04/diffusion-for-recsys/)

## Semaine 1 (2024-05-06)

### Objectifs

- Prendre en main les outils qui seront utilisés pour le projet
- Produire une première version de l'échéancier
- Étudier le domaine, les notions et outils envisagés pour le projet

### Réalisations

<!-- Description des tâches accomplies -->
- **Planification du projet**: Définition des grandes tâches à effectuer durant la session.
- **Recherche de sources pour la ceuillette des données**: Recherche de quelques bases de données pour la récupération ainsi que la validation des attributs des différents repas. Recherche de bases de données pour tester le système.

<!-- ### Observations -->
<!-- Description des observations importantes (ex: remarque ou trouvaille intéressante, difficultés rencontrées) de la semaine -->


### Ressources
- [Description des algorithmes de recommandation](https://towardsdatascience.com/introduction-to-recommender-systems-1-971bd274f421)
- [Implémentation des algorithmes en python](https://www.geeksforgeeks.org/recommendation-system-in-python/)
- [Market Basket Analysis](https://www.youtube.com/watch?v=icGS26TS1fE&ab_channel=DATAtab)
- [Market Basket Analysis python](https://medium.com/@jihargifari/how-to-perform-market-basket-analysis-in-python-bd00b745b106)
- [Base de données de test](https://www.kaggle.com/datasets/joebeachcapital/fast-food)
- [Plateforme pour receuillir les informations sur les repas (Fatsecret)](https://platform.fatsecret.com/)