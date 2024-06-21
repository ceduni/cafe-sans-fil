# Format et ceuillette des données
Cette page vise à présenter quel formats les données devraient avoir ainsi qu'une 
description de comment ces données peuvent être obtenus.

## Source des données
- Historique d’achat de l'utilisateur
- Likes
- Commentaires

## Format des données

**Item**
```
{
    "barecode": "String",
    "item_id": "UUID",
    "health_score": "Decimal128",
    "time": "String",
    "likes": ["String"],
    "diet": ["String"],
    "allergens": ["String"],
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

**User**
```
{  
    "order_history": ["Order"],
    "dietary_profile": {
        "diets": ["String"],
        "foods_categories": ["String"],
        "nutrients": ["String"],
        "allergens": [
            {
                "names": ["String"],
                "danger_level": ["Int32"]
            }
        ]
    }
}
```

**Users recommendations**
```
{
    "user_id": {
        "cafe_slug": [
            {
                "barecode": "String",
                "item_id": "UUID",
                "health_score": "Decimal128",
                "time": "String",
                "likes": ["String"],
                "diet": ["String"],
                "allergens": ["String"],
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
        ],
    },

    "healthy_recommendations": [
        "cafe_slug": [
            {
                "barecode": "String",
                "item_id": "UUID",
                "health_score": "Decimal128",
                "time": "String",
                "likes": ["String"],
                "diet": ["String"],
                "allergens": ["String"],
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
        ]
    ]
}
```

**Public recommendations**
```
{
    "cafe_slug": [
        {
            "barecode": "String",
            "item_id": "UUID",
            "health_score": "Decimal128",
            "time": "String",
            "likes": ["String"],
            "diet": ["String"],
            "allergens": ["String"],
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
    ],

    "healthy_recommendations": [
        "cafe_slug": [
            {
                "barecode": "String",
                "item_id": "UUID",
                "health_score": "Decimal128",
                "time": "String",
                "likes": ["String"],
                "diet": ["String"],
                "allergens": ["String"],
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
        ]
    ]
}
```