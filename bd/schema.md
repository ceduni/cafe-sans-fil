# 🗃️ BD (Base de Données)

Ce document présente la structure de notre BD MongoDB.

## Collections


### Users

- `_id`: ObjectId
- `udem_email`: EmailStr (unique)
- `first_name`: String
- `last_name`: String
- `roles`: Array of Objects
  - `cafe_id`: ObjectId
  - `role_type`: String ('benevole', 'admin')

### Cafés

- `_id`: ObjectId
- `name`: String
- `description`: String
- `faculty`: String
- `location`: String
- `email`: EmailStr
- `phone_number`: String (optional)
- `website`: String (optional)
- `facebook`: String (optional)
- `instagram`: String (optional)
- `image_url`: String (optional)
- `is_open`: Boolean
- `opening_hours`: Array of Objects
  - `day`: String
  - `open`: Time
  - `close`: Time
- `payment_methods`: Array of Objects
  - `method`: String
  - `minimum`: Float (optional)

### MenuItems

- `_id`: ObjectId
- `cafe_id`: ObjectId (Reference to Café)
- `name`: String
- `description`: String
- `price`: Float
- `image_url`: String (optional)
- `is_available`: Boolean
- `category`: String

### Orders

- `_id`: ObjectId
- `user_id`: ObjectId (Reference to User)
- `cafe_id`: ObjectId (Reference to Café)
- `items`: Array of Objects
  - `item_id`: ObjectId
  - `quantity`: Int
  - `item_price`: Float
- `total_price`: Float
- `status`: String ('active', 'pending', 'completed', 'cancelled')
- `order_timestamp`: DateTime
- `pickup_timestamp`: DateTime