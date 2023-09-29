# Flux

Ce document présente les différents flux de données et leur output, afin de préparer les routes d'API.

## 1. Authentification & Autorisation

> Le flux débute lorsque l'utilisateur clique sur le bouton "Connexion" ou "Inscription" dans le menu de navigation.

<img width="609" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/a9d6bf6f-ae22-45d9-809b-61ba3040830b">

### Input

#### Register

> Cette étape débute lorsque l'utilisateur clique sur le bouton "Inscription" dans le menu de navigation.

```json
{ "matricule": "123456", "email": "johndoe@umontreal.ca", "password": "securePass123" }
```

#### Login

> Cette étape débute lorsque l'utilisateur clique sur le bouton "Connexion" dans le menu de navigation.

```json
{ "matricule": "123456", "password": "securePass123" }
```

### Output

```json
{
  "token": "xyz123456abcdef",
  "user": {
    "id": "123456",
    "email": "johndoe@umontreal.ca",
    "role": "client"
  }
}
```

## 2. Présentation des cafés

> Le flux débute dès la page d'accueil, connecté ou non.

<img width="474" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/59c544ac-79a1-42da-af7e-031c8e3c28ed">

### Output

#### Fetch full list

> Cette étape débute au chargement de la page d'accueil.

```json
{
    "cafes":
        [
            {
                "id": 1,
                "name": "Café Central",
                "description": "A cozy cafe in the city center",
                "photo": "link_to_photo"
            },
            {
                "id": 2,
                "name": "Café Tore et Fraction",
                "description": "Le café Tore est un café étudiant situé au pavillon André-Aisenstadt.",
                "photo": "link_to_photo"
            }
            ...
        ]
}
```

#### Fetch single cafe, selected by id

> Cette étape débute lorsque l'utilisateur clique sur un café dans la liste.

```json
{
  "id": 2,
  "name": "Café Tore",
  "description": "Le café Tore est un café étudiant situé au pavillon André-Aisenstadt.",
  "photo": "link_to_photo",
  "open": true,
  "openingHours": {
    "monday": { "open": "08:00", "close": "17:00" },
    "tuesday": { "open": "08:00", "close": "17:00" },
    "wednesday": { "open": "08:00", "close": "17:00" },
    "thursday": { "open": "08:00", "close": "17:00" },
    "friday": { "open": "08:00", "close": "17:00" },
    "saturday": { "open": "08:00", "close": "17:00" },
    "sunday": { "open": "08:00", "close": "17:00" }
  },
  "paymentMethods": ["cash", "debit", "credit"],
  "minimumCardAmount": 5.0
}
```

## 3. Recherche

> Le flux débute lorsque l'utilisateur clique sur le champ de recherche.

<img width="474" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/592156d1-61b3-47e2-a257-41961970f3c2">

### Input

```json
{ "query": "Café Tore et Fraction" }
```

### Output

#### Search for a cafe

> Cette étape débute lorsque l'utilisateur a fini de taper sa recherche.

```json
{
  "results": [
    {
      "id": 2,
      "name": "Café Tore et Fraction",
      "description": "Le café Tore est un café étudiant situé au pavillon André-Aisenstadt.",
      "photo": "link_to_photo"
    }
  ]
}
```

#### Select cafe from search result

> Cette étape débute lorsque l'utilisateur clique sur un café depuis les résultats de recherche.

[See above](#fetch-single-cafe-selected-by-id)

## 4. Menu des cafés

> Le flux débute lorsque l'utilisateur clique sur le bouton "Menu" dans la page d'un café.

<img width="474" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/8bffa692-368c-40d2-b286-85e63c08a721">

### Output

#### Fetch cafe menu

> Cette étape débute au chargement de la page du menu.

```json
[
    {
        "itemId": 1,
        "name": "Espresso",
        "description": "Strong coffee made by forcing steam through finely-ground coffee beans.",
        "price": 2.5,
        "photo": "link_to_espresso_photo"
    },
    {
        "itemId": 2,
        "name": "Cappuccino",
        "description": "Coffee made with milk that has been frothed up with pressurized steam.",
        "price": 3.5,
        "photo": "link_to_cappuccino_photo"
    },
    ...
]
```

#### Fetch single menu item, selected by id

> Cette étape débute lorsque l'utilisateur clique sur un item dans le menu.

```json
{
  "itemId": 1,
  "name": "Espresso",
  "description": "Strong coffee made by forcing steam through finely-ground coffee beans.",
  "price": 2.5,
  "photo": "link_to_espresso_photo",
  "ingredients": ["Water", "Espresso Beans"],
  "calories": 10,
  "vegan": true,
  "available": true
}
```

## 5. Passation de commandes

> Le flux débute lorsque l'utilisateur clique sur le bouton "Commander" dans la page d'un café.

<img width="832" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/31e97630-2ff7-4524-bc8c-a434cd8ed05b">

### Input

#### Add item to cart

> Cette étape débute lorsque l'utilisateur ajoute un item à son panier.

```json
{ "cart": [{ "itemId": 1, "quantity": 2 }] }
```

#### Review and confirm order

> Cette étape débute lorsque l'utilisateur clique sur le bouton "Commander" dans son panier.

```json
{
  "orderId": 12345,
  "totalAmount": 9.98,
  "items": [
    { "itemId": 1, "quantity": 2, "price": 2.5 },
    { "itemId": 2, "quantity": 1, "price": 4.99 }
  ]
}
```

#### See order history

> Cette étape débute lorsque l'utilisateur clique sur le bouton "Historique" sur la page de son profil.

```json
{ "orders": [ { "orderId": 12345, "date": "2023-09-23", "totalAmount": 9.98, ... }, ... ] }
```

## 6. Traitement des commandes (Staff)

> Le flux débute lorsque le staff clique sur le bouton "Commandes" dans le menu de navigation, ou qu'il reçoit une notification.

<img width="453" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/91cb9dd0-e5fd-4333-bc2d-f4318b000eb2">

### Input

#### Update order status

> Cette étape débute lorsque le staff modifie le statut d'une commande depuis la page "Commandes".

```json
{ "orderId": 1001, "status": "processed" }
```

### Output

#### View incoming orders

> Cette étape débute lorsque le staff clique sur le bouton "Commandes" dans le menu de navigation, ou qu'il clique sur une notification.

```json
[
    {
        "orderId": 1001,
        "userId": 45,
        "items": [ {"itemId": 1, "quantity": 2}, {"itemId": 2, "quantity": 1} ],
        "status": "pending",
        "totalPrice": 8.5
    },
    ...
]
```

## 7. Gestion de menu (Staff)

> Le flux débute lorsque le staff clique sur le bouton Modifier le menu depuis la page de gestion d'un de ses cafés.

<img width="626" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/14ff638b-ef68-4cd0-a511-92bdeb9f34f2">

### Input

#### Add item to menu

> Cette étape débute lorsque le staff ajoute un item au menu.

```json
{ "name": "Latte", "description": "Coffee with steamed milk.", "price": 3.0, "photo": "link_to_latte_photo" }
```

#### Modify item in menu

> Cette étape débute lorsque le staff modifie un item du menu.

```json
{
  "name": "Latte",
  "description": "Delicious coffee with steamed milk.",
  "price": 3.5,
  "photo": "link_to_updated_latte_photo"
}
```

## 8. Gestion de l'inventaire (Staff)

> Le flux débute lorsque le staff clique sur le bouton "Inventaire" dans la page de gestion d'un de ses cafés.

<img width="450" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/97dfa692-9c9f-407b-97b0-5cf7b3c07a92">

### Input

#### Update inventory

> Cette étape débute lorsque le staff modifie la quantité d'un item dans l'inventaire.

```json
{ "itemId": 1, "quantity": 10 }
```

### Output

#### Get current inventory

> Cette étape débute lorsque le staff clique sur le bouton "Inventaire" dans la page de gestion d'un de ses cafés.

```json
[
    {
        "itemId": 1,
        "quantity": 10
    },
    {
        "itemId": 2,
        "quantity": 5
    },
    ...
]
```

## 9. Gestion du personnel (Admin)

> Le flux débute lorsque l'admin clique sur le bouton "Gestion du personnel" dans la page de gestion d'un de ses cafés.

<img width="589" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/07936f83-d718-40e8-bf1e-5991215cff9f">

### Input

#### Add staff member

> Cette étape débute lorsque l'admin ajoute un membre du staff.

```json
{ "matricule": "123456", "role": "Bénévole", "cafeId": 1 }
```

#### Update staff member

> Cette étape débute lorsque l'admin modifie un membre du staff.

```json
{ "matricule": "123456", "role": "Admin", "cafeId": 1 }
```

## 10. Rapports (Admins and Staff)

> Le flux débute lorsque l'admin clique sur le bouton "Rapports" dans la page de gestion d'un de ses cafés.

<img width="301" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/a8113f9c-bc3e-4f3d-b8ed-bf96cff0d85e">

### Input

#### Select report criteria

> Cette étape débute lorsque l'admin sélectionne les critères de son rapport.

```json
{ "type": "sales", "dateRange": { "start": "2023-09-01", "end": "2023-09-30" } }
```

### Output

#### Get reports

> Cette étape débute lorsque l'admin clique sur le bouton "Générer" dans la page de rapports.

```json
{
    "startDate": "2023-09-01",
    "endDate": "2023-09-30",
    "totalSales": 1500,
    "totalOrders": 180,
    "itemsSold": [
            {
                "itemId": 101,
                "itemName": "Café Latte",
                "quantity": 85,
                "total": 425
            }, {
                "itemId": 102,
                "itemName": "Mocha",
                "quantity": 40,
                "total": 200
            }, ...
        ]
}
```
