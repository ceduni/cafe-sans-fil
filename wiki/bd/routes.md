# 🌐 Routes (API)

Ce document présente les routes de notre API.

## Cafés

- **GET** `/api/cafes`: List all cafés.
- **GET** `/api/cafes/{cafe_id}`: Retrieve detailed information about a café.
- **POST** `/api/cafes`: Create a new café.
- **PUT** `/api/cafes/{cafe_id}`: Update a café's information (Admin only).

## Menus

- **GET** `/api/cafes/{cafe_id}/menu`: Retrieve the menu of a café.
- **GET** `/api/cafes/{cafe_id}/menu/{item_id}`: Get a specific menu item.
- **POST** `/api/cafes/{cafe_id}/menu`: Add an item to the menu (Admin).
- **PUT** `/api/cafes/{cafe_id}/menu/{item_id}`: Update a menu item (Admin).
- **DELETE** `/api/cafes/{cafe_id}/menu/{item_id}`: Delete a menu item (Admin).

## Search

- **GET** `/api/search?query=<search_query>&category=<category>&is_available=<true/false>&is_open=<true/false>`: Unified search for both items and cafés. The category, is_available, and is_open parameters are optional.

## Users

- **GET** `/api/users/{user_id}`: Retrieve a user’s details, including their name, email...
- **POST** `/api/users`: Create a user.
- **PUT** `/api/users/{user_id}`: Update a user's details or roles.

## Orders

- **POST** `/api/orders`: Place a new order.
- **GET** `/api/orders/{order_id}`: Retrieve order details.
- **PUT** `/api/orders/{order_id}`: Update an order's status (Bénévole/Admin), including marking as "cancelled".
- **GET** `/api/users/{user_id}/orders?status=<status>`: Retrieve a user's orders, with status filtering.
- **GET** `/api/cafes/{cafe_id}/orders?status=<status>`: Retrieve a café's orders, with status filtering.