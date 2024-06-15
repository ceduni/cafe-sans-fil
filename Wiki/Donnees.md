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
    "time": "String",
    "likes": ["String"],
    "nombre_likes": "Decimal128,
    "category": "String",
    "regime_alimentaire": "String",
    "nutritionnal_information": {
        "protein": "Decimal128",
        "lipids": "Decimal128",
        "carbohydrates": "Decimal128",
        "fiber": "Decimal128",
        "vitamins": "Decimal128",
        "sugar": "Decimal128",
        "sodium": "Decimal128",
        "energy_per_100g": "Decimal128",
        "saturated fatty acids": "Decimal128",
    }
}
```

**Users**
```
{  
    "order_history": [
        {
            "order_id": "UUID",
            "item_id": "UUID",
            "cafe_id": "UUID"
        }
    ],
    
    "allergens": {
        "names": ["String"],
        "level": ["Int32"]
    },
}
```
