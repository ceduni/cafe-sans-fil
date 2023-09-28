# Flux

Ce document présente les différents flux de données et leur output, afin de préparer les routes d'API.

## 1. Authentification & Autorisation

<img width="609" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/a9d6bf6f-ae22-45d9-809b-61ba3040830b">

### Input

#### Register

```json
{ "matricule": "123456", "email": "johndoe@umontreal.ca", "password": "securePass123" }
```

#### Login

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

<img width="474" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/59c544ac-79a1-42da-af7e-031c8e3c28ed">

### Output

#### Fetch full list

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

<img width="474" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/592156d1-61b3-47e2-a257-41961970f3c2">

### Input

```json
{ "query": "Café Tore et Fraction" }
```

### Output

#### Search for a cafe

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

[See above](#fetch-single-cafe-selected-by-id)

## 4. Menu des cafés

<img width="474" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/8bffa692-368c-40d2-b286-85e63c08a721">

### Output

#### Fetch cafe menu

```json
[
    {
        "itemId": 001,
        "name": "Espresso",
        "description": "Strong coffee made by forcing steam through finely-ground coffee beans.",
        "price": 2.5,
        "photo": "link_to_espresso_photo"
    },
    {
        "itemId": 002,
        "name": "Cappuccino",
        "description": "Coffee made with milk that has been frothed up with pressurized steam.",
        "price": 3.5,
        "photo": "link_to_cappuccino_photo"
    },
    ...
]
```

#### Fetch single menu item, selected by id

```json
{
  "itemId": 001,
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

<img width="832" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/31e97630-2ff7-4524-bc8c-a434cd8ed05b">

## 6. Traitement des commandes (Staff)

<img width="453" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/91cb9dd0-e5fd-4333-bc2d-f4318b000eb2">

## 7. Gestion de menu (Staff)

<img width="626" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/14ff638b-ef68-4cd0-a511-92bdeb9f34f2">

## 8. Gestion de l'inventaire (Staff)

<img width="450" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/97dfa692-9c9f-407b-97b0-5cf7b3c07a92">

## 9. Gestion du personnel (Admin)

<img width="589" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/07936f83-d718-40e8-bf1e-5991215cff9f">

## 10. Rapports (Admins and Staff)

<img width="301" alt="image" src="https://github.com/ceduni/udem-cafe/assets/83944331/a8113f9c-bc3e-4f3d-b8ed-bf96cff0d85e">
