# 🗃️ Schemas (Base de Données)

Ce document présente la structure de notre BD MongoDB.

## Collections

### User

```json
{
  "user_id": "Binary (UUID unique)",
  "email": "String (unique, indexed)",
  "matricule": "String (unique, indexed)",
  "username": "String (unique, indexed)",
  "hashed_password": "String",
  "first_name": "String (indexed)",
  "last_name": "String (indexed)",
  "photo_url": "String (optional)",
  "is_active": "Boolean"
}
```

<br>

### Cafe

```json
{
  "cafe_id": "Binary (UUID unique)",
  "name": "String (unique, indexed)",
  "description": "String (indexed)",
  "image_url": "String (optional)",
  "faculty": "String (indexed)",
  "is_open": "Boolean",
  "status_message": "String (optional)",
  "opening_hours": [
      {
          "day": "String",
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
          "start": "Date (optional)",
          "end": "Date (optional)"
      }
  ],
  "staff": [
      {
          "user_id": "Binary (UUID)",
          "role": "String (Enum values: 'Bénévole', 'Admin')"
      }
  ],
  "menu_items": [
      {
          "item_id": "Binary (UUID unique)",
          "name": "String (unique, indexed)",
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
.  
<br>

### Order

```json
{
  "order_id": "Binary (UUID unique)",
  "user_id": "Binary (UUID)",
  "cafe_id": "Binary (UUID)",
  "items": [
    {
      "item_id": "Binary (UUID)",
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
  "status": "String (Enum values: 'Placée', 'Prête', 'Complétée', 'Annulée')",
  "created_at": "Date",
  "updated_at": "Date"
}
```

