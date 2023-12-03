# 🗃️ Schemas

Ce document présente la structure de notre BD MongoDB.

Pour plus de détails sur les routes et les fonctionnalités de notre API, vous pouvez consulter notre documentation disponible via Swagger UI et ReDoc aux adresses suivantes :  

- Swagger UI : [cafesansfil-api.onrender.com/docs](https://cafesansfil-api.onrender.com/docs)  
- ReDoc : [cafesansfil-api.onrender.com/redoc](https://cafesansfil-api.onrender.com/redoc)  

## Collections

### User

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

### Cafe

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

### Order

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

