# Format et ceuillette des données
Cette page vise à présenter quel formats les données devraient avoir ainsi qu'une 
description de comment ces données peuvent être obtenus.

## Source des données
- Historique d’achat de l'utilisateur
- Likes
- Commentaires

## Format des données

**Food**
```
{
    "barecode": "String",
    "item_id": "UUID",
    "health_score": "Decimal128",
    "allergens": ["String"].
    "time": "String",
    "likes": ["String"],
    "nombre_likes": "Decimal128,
    "nutritionnal_densities": {
        "protein": "Decimal128",
        "lipids": "Decimal128",
        "carbohydrates": "Decimal128"
    }
}
```

**Users**
```
{
  "likes": [
        {
            "barecode": "String",
            "item_id": "UUID",
            "health_score": "Decimal128",
            "allergens": ["String"].
            "time": "String",
            "likes": "["String"]",
            "nutritionnal_densities": {
                "protein": "Decimal128",
                "lipids": "Decimal128",
                "carbohydrates": "Decimal128"
            }
        }
    ],
    
    "allergens": {
        "names": ["String"],
        "level": ["Int32"]
    },

    "historique_achat": [
        {
            "barecode": "String",
            "item_id": "UUID",
            "health_score": "Decimal128",
            "allergens": ["String"].
            "time": "String",
            "likes": "["String"]",
            "nutritionnal_densities": {
                "protein": "Decimal128",
                "lipids": "Decimal128",
                "carbohydrates": "Decimal128"
            }
        }
    ]
}
```