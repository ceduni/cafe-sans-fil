# Logique de fonctionnement des systèmes de recommandation
Cette page présente les différents algorithmes utilisés dans le système de recommandation.

## 0. Heuristiques de recommandations:

1. ***Heure de la journée :*** permet d'approximer les besoins énergétiques
2. ***Valeurs nutritives :*** permet de déterminer les apports du repas
3. ***Catégorie de repas :*** permet de hiérarchiser les repas (prendre en compte le temps de digestion)
4. ***Fraîcheur des aliments :*** (fraîcheur des aliments  après leur arrivés au café) -> permet d'approximer la qualité du repas
5. ***Préférence de l'individu :*** permet de personnaliser et classer les recommandations


## 1. Prétraitement et formattage des données
Pour chaque repas du menu:

1. Calculer la densité en sucre, protéine, en lipide, glucide, vitamines et sodium etc. et le niveau hiérarchique.
2. Calculer son score santé (**section 3**).
3. Attribuer une étiquette disant à quel moment de la journée le repas devrait être consommé (**section 2.6**).
1. Mettre les repas dans le bon format (voir fichier ***Donnees.md***).

## 2. Algorithmes secondaires

### 2.1 Obtenir les préférences à partir du profile

Profile nutritif: 
1. Principaux régime alimentaire ([référence](https://larecolteenvrac.com/articles/les-differents-regimes-alimentaires)):
    1. Végétarisme
    2. Végétalisme
    3. Véganisme
    4. Sans lactose
    5. Sans gluten
    6. Cétogène
2. Catégories des repas
3. Précision des valeurs nutritives (l'utilisateur veut des repas avec beaucoup de protéines etc.)

### 2.2 Trouver les repas contenant les allergènes spécifiés par l’utilisateur (appel uniquement lors du changement dans la spécification des allergènes)

Niveau allergies:

I- Supportable, rien de très grave

II- Assez inconfortable mais pas mortel

III- Très grave, possiblement mortel, ne doit jamais consommer

1. Entrée: liste des allergènes de l’utilisateur (dans l’ordre de gravité)
2. Pour chaque repas du menu, vérifier si l’un des allergènes se trouve dans la liste des allergènes contenu dans le repas (allergènes des repas est fourni par Fatsecret)
    1. Classer les repas contenant des allergènes par ordre de gravité
3. Retourner les repas allergènes


### 2.3 Déterminer les habitudes de consommation (pour les heures de la journée)
1. Récupérer les repas les plus consommés en fonction de l'heure de la journée.
2. Pour chaque intervalle d'heure (**à déterminer**), trouver le repas le plus acheté
3. Retourner ces repas (ce sont les représentant de chaque)

<!--
Avis Nutrotionniste
### 2.6 Attribuer un moment de la journée à un repas
1. Entrée: un repas
2. Définir les étiquettes. ***TODO: Définir les intervalles d'heure***
3. Définir n ensemble(s) qui représentent les repas qui devraient être consommés à n moment de la journée (un ensemble pour les repas qui devraient être consommés entre 8h-10h AM etc.).
4. Mettre chaque aliment dans le bon cluster en fonction de la densité en protéine, lipide et en glucide ainsi que de son apport en calories (voir référence 8).
5. Pour chaque élément dans le même cluster, attribuer une étiquette (***à définir***).
-->

## 3. Robot de recommandation de repas santé

### 3.1 Définition du score de santé

#### **Hiérarchie des repas**

1. Aliments non transformés:
    - fruits et légumes frais
    - noix, graines et eau
    - etc
2. Aliments minimalement transformés: 
    - …
3. Aliments transformés
    - …
4. Aliments ultra transformés
    - certaines céréales à déjeuner
    - certains pains industriels, craquelins, croustilles, grignotines salées
    - biscuits, barres tendres, friandises chocolatées, gâteaux, bonbons…
    - repas surgelés (pizzas, croquettes, pâtes…)
    - saucisses, viandes froides, soupes instantanées…
    - boissons sucrées (boissons gazeuses et énergisantes, cocktail de fruits…)

#### **Scores**

- **Fraîcheur pour un aliment:**
    1. Récupérer l’aliment ( avec la date à laquelle il a été mit dans le stock ainsi que sa data d’expiration )
    2. Soit ***t*** le nombre de jours écoulés depuis l’ajout de l’aliment dans le stock et ***T*** la durée de conservation restante (à partir de l’ajout dans le stock jusqu’à la date d’expiration)
    3. Retourner $\displaystyle Score = e^{-\frac{t}{T}}$.
    
- **Hiérarchie**

    | Hiérarchie | Score |
    | --- | --- |
    | 1 | 1 |
    | 2 | 0.5 |
    | 3 | -0.5 |
    | 4 | -2 |
    
- [**Nutri-score**](https://en.wikipedia.org/wiki/Nutri-Score)


#### **Fonction de score finale**

- X % score fraîcheur
- Y % score densité nutritionnelle
- Z % score hiérarchie
- W % score hiérarchie

### 3.2 Conception du robot
1. En fonction du moment de la journée, trouver le bon ensemble de repas et retourner les k repas avec le plus haut score santé.

## 4. Algorithmes principales

### 4.1 Collaborative Filtering (recommandation individuelle)

1. Liste L contenant les candidats de recommandation
2. Récupérer aléatoirement un sous ensemble $S$, de taille n, des utilisateurs $\text{ tq } u \notin S$ où $u$ représente l’utilisateur courant
3. Récupérer l’ensemble $U$ des repas aimés par l’utilisateur $u$ et l’ensemble $X$ des repas aimés par un autre utilisateur $x\in S$
4. Calculer $Jaccard(U, X)$ (mesure de similarité)
5. S’ils sont assez similaires, récupérer la liste des k repas aimés par $x$ qui n’ont pas encore été achetés par $u$ et les rajouter dans L
6. Retirer utilisateur $x$ de $S$ et recommencer à 3. jusqu’à ce qu’il n’y ait plus d’éléments dans $S$
7. Utiliser une fonction de score pour garder les p repas possédant les plus haut scores et les recommander

### 4.2 Content Based Filtering (recommandation individuelle)

1. Liste L contenant les candidats de recommandation
2. Récupérer le(s) k cluster(s) qui représente(nt) le mieux les préférences de l’utilisateur OU/ET les clusters qui contiennent le plus de repas aimés
3. Récupérer aléatoirement un échantillon $E_i$ de taille n dans chaque cluster
4. Créer une matrice $X_{nk\times p}$ où $nk$ est le nombre de repas (lignes) et p, le nombre d’attributs (*****à déterminer***** )
5. Compléter la matrice comme suit : $X_{ij} = 0$ si le repas $i$ n'a pas l'attribut $j$ et $X_{ij} = 1$ sinon
6. Récupérer un repas aimé par l’utilisateur qui est dans $\cup E_i,..., E_k$
7. Créer un vecteur V tel que l’élément i de V corresponde au nombre de match que les lignes 1 et $i\text{ }(i > 1$) de X possèdent (ie. le nombre d’index pour lesquels les deux vecteurs contiennent la même valeur 0 ou 1) où la ligne 1 de X représente le repas trouvé en 6.
8. S’il y a un seule cluster, rajouter les *m* repas possédant le plus grand coefficient de V dans L. Sinon, rajouter le repas avec le plus grand coefficient dans L et recommencer à l’étape 4. avec un autre échantillon.
9. Utiliser une fonction de score pour garder les p repas possédant les plus haut scores et les recommander

### 4.3 Knowledge Based Recommender (recommandation individuelle)

1. Récupérer les repas allergènes par **2.2** et garder les repas de niveau II et III.
2. Classer ces repas en fonction de leur catégories.
3. Récupérer les préférences de l’utilisateur par 2.1 (liste de préférence).
4. Récupérer les repas qui respectent les préférences de l'utilisateur.
5. Retirer tous les repas allergènes des repas trouvés en 4.
6. Utiliser une fonction de score pour garder les p repas possédant les plus haut scores et les recommander.

### 4.4 Recommandation globale (ensemble des utilisateurs)

1. Récupérer les k repas possédant le plus de likes dans le menu.
2. Récupérer les p repas les plus consommés en fonction de l'heure de la journée (faire un appel avec l'API).
3. Regrouper les repas qui devraient être consommés durant la même période de la journée ensemble.
4. En fonction de l'heure de la journée, retourner le bon cluster.

<!--
### 4.5 Recommandation de café basé sur la recherche de repas

1. Liste *L* des cafés
2. Récupérer le repas recherché (R)
3. Récupérer les menus de tous les cafés (map M)
4. Rajouter tous les restaurants dans lesquels R est vendu dans la liste *L*
5. Retourner L
-->

# Références

1. [Lien Medium](https://towardsdatascience.com/introduction-to-recommender-systems-1-971bd274f421): Description des systèmes de recommandation.
2. [Geeks for Geeks](https://www.geeksforgeeks.org/recommendation-system-in-python/): Implémentation d'un système en python.
3. [Market Basket Analysis description](https://www.youtube.com/watch?v=icGS26TS1fE&ab_channel=DATAtab), [MBA python](https://medium.com/@jihargifari/how-to-perform-market-basket-analysis-in-python-bd00b745b106): Intéressant pour voir la relation entre les repas (quel repas est souvent consommé avec quel repas etc.) pour l’utilisateur.
4. [Base de donnée de test](https://www.kaggle.com/datasets/joebeachcapital/fast-food)
5. [Fatsecret](https://platform.fatsecret.com/)
6. [Python Machine Learning - K-means (w3schools.com)](https://www.w3schools.com/python/python_ml_k-means.asp)
7. [Comprendre la densité nutritionnelle | Ethiquable](https://www.ethiquable.coop/page-guide-dachats-espace-presse/comprendre-densite-nutritionnelle#:~:text=Il%20existe%20plusieurs%20d%C3%A9finitions%20mais,%C3%A0%20son%20contenu%20en%20calories.)
8. [Comment organiser sa journée et sa répartition calorique](https://media.dietis.fr/sante-et-alimentation/conseils-nutrition-sante/893-repartition-calorique-quotidienne.html)
9. [Nutri-score](https://en.wikipedia.org/wiki/Nutri-Score)