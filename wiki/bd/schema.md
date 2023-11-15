# 🗃️ Schemas (Base de Données)

Ce document présente la structure de notre BD MongoDB.

## Collections

### User

```json
{
  "user_id": "UUID (unique)",
  "email": "string (unique, indexed)",
  "matricule": "string (unique, indexed)",
  "username": "string (unique, indexed)",
  "hashed_password": "string",
  "first_name": "string (indexed)",
  "last_name": "string (indexed)",
  "photo_url": "string (optional)",
  "is_disabled": "boolean (optional)"
}
```

<br>

### Cafe

```json
{
  "cafe_id": "UUID (unique)",
  "name": "string (unique, indexed)",
  "description": "string (indexed)",
  "image_url": "string (optional)",
  "faculty": "string (indexed)",
  "is_open": "boolean",
  "opening_hours": [
      {
          "day": "string",
          "blocks": [
              {
                  "start": "string (HH:mm format)",
                  "end": "string (HH:mm format)"
              }
          ]
      }
  ],
  "location": {
      "pavillon": "string (indexed)",
      "local": "string (indexed)"
  },
  "contact": {
      "email": "string (optional, email format)",
      "phone_number": "string (optional)",
      "website": "string (optional)"
  },
  "social_media": [
      {
          "platform_name": "string",
          "link": "string"
      }
  ],
  "payment_methods": [
      {
          "method": "string",
          "minimum": "double (optional)"
      }
  ],
  "additional_info": [
      {
          "type": "string",
          "value": "string",
          "start": "Date (optional)",
          "end": "Date (optional)"
      }
  ],
  "staff": [
      {
          "user_id": "UUID",
          "role": "string (Enum values: 'Bénévole', 'Admin')"
      }
  ],
  "menu_items": [
      {
          "item_id": "UUID (unique)",
          "name": "string (unique, indexed)",
          "tags": ["string"],
          "description": "string (indexed)",
          "image_url": "string (optional)",
          "price": "double",
          "is_available": "boolean",
          "category": "string (indexed)",
          "options": [
              {
                  "type": "string",
                  "value": "string",
                  "fee": "double"
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
  "order_id": "UUID (unique)",
  "user_id": "UUID",
  "cafe_id": "UUID",
  "items": [
    {
      "item_id": "UUID",
      "quantity": "int",
      "item_price": "double",
      "options": [
        {
          "type": "string",
          "value": "string",
          "fee": "double"
        }
      ]
    }
  ],
  "total_price": "double",
  "status": "string (Enum values: 'Placée', 'Prête', 'Complétée', 'Annulée')",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

