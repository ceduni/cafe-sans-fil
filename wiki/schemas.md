> Notre documentation de l'API back-end est disponible via Swagger UI et ReDoc aux URL suivantes :  
>   
> - Swagger UI : [cafesansfil-api.onrender.com/docs](https://cafesansfil-api.onrender.com/docs)  
> - ReDoc : [cafesansfil-api.onrender.com/redoc](https://cafesansfil-api.onrender.com/redoc) 

# 🗃️ Schemas

Ce document présente la structure de notre BD MongoDB.

## Collections

### users

```json
{
  "user_id": "UUID",
  "email": "String (unique, indexed, email format)",
  "matricule": "String (unique, indexed)",
  "username": "String (unique, indexed)",
  "hashed_password": "String",
  "first_name": "String (indexed)",
  "last_name": "String (indexed)",
  "photo_url": "String (optional)",
  "failed_login_attempts": "Int32",
  "last_failed_login_attempt": "DateTime (optional)",
  "lockout_until": "DateTime (optional)",
  "is_active": "Boolean"
}
```

### cafes

```json
{
  "cafe_id": "UUID",
  "name": "String (unique, indexed)",
  "slug": "String (unique, indexed)",
  "description": "String (indexed)",
  "image_url": "String (optional)",
  "faculty": "String (indexed)",
  "is_open": "Boolean",
  "status_message": "String (optional)",
  "opening_hours": [
      {
          "day": "Enum (Days of week)",
          "blocks": [
              {
                  "start": "String (HH:mm format)",
                  "end": "String (HH:mm format)"
              }
          ]
      }
  ],
  "location": {
      "pavillon": "String (indexed)",
      "local": "String (indexed)"
  },
  "contact": {
      "email": "String (optional, email format)",
      "phone_number": "String (optional)",
      "website": "String (optional)"
  },
  "social_media": [
      {
          "platform_name": "String",
          "link": "String"
      }
  ],
  "payment_methods": [
      {
          "method": "String",
          "minimum": "Decimal128 (optional)"
      }
  ],
  "additional_info": [
      {
          "type": "String",
          "value": "String",
          "start": "DateTime (optional)",
          "end": "DateTime (optional)"
      }
  ],
  "staff": [
      {
          "username": "String (unique, indexed)",
          "role": "Enum ('Bénévole', 'Admin')"
      }
  ],
  "menu_items": [
      {
          "item_id": "UUID",
          "name": "String (unique, indexed)",
          "slug": "String (optional, unique, indexed)",
          "tags": ["String"],
          "description": "String (indexed)",
          "image_url": "String (optional)",
          "price": "Decimal128",
          "in_stock": "Boolean",
          "category": "String (indexed)",
          "options": [
              {
                  "type": "String",
                  "value": "String",
                  "fee": "Decimal128"
              }
          ]
      }
  ]
}

```

### orders

```json
{
  "order_id": "UUID",
  "order_number": "Int32 (unique, indexed)",
  "cafe_name": "String",
  "cafe_slug": "String",
  "cafe_image_url": "String (optional)",
  "user_username": "String",
  "items": [
    {
      "item_name": "String",
      "item_slug": "String",
      "item_image_url": "String (optional)",
      "quantity": "Int32",
      "item_price": "Decimal128",
      "options": [
        {
          "type": "String",
          "value": "String",
          "fee": "Decimal128"
        }
      ]
    }
  ],
  "total_price": "Decimal128",
  "status": "Enum ('Placée', 'Prête', 'Complétée', 'Annulée')",
  "created_at": "DateTime",
  "updated_at": "DateTime"
}
```


### Notes sur les Statuts de Commande

Chaque commande traverse différents statuts qui indiquent sa progression :

- **🔄 Placée**: 
  - **Définition** : La commande est enregistrée mais n'est pas encore traitée par le café.
  
- **✅ Prête**: 
  - **Définition** : La commande a été traitée et est prête à être récupérée par le client.

- **✔️ Complétée**: 
  - **Définition** : La commande a été récupérée par le client et est considérée comme terminée.

- **❌ Annulée**: 
  - **Définition** : La commande a été annulée.
  - **Détails** : 
    - Peut se produire automatiquement si la commande n'est pas traitée ou récupérée dans le délai d'une heure.
    - Peut également être annulée manuellement par le client ou le café pour diverses raisons, telles que l'indisponibilité d'un article ou un autre problème opérationnel.
