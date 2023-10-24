# 🌐 Routes (API)

Ce document présente les routes de notre API.

## Cafés

- **GET** `/api/cafes?is_open=<true/false>&payment_method=<method>`: List all cafés.
- **GET** `/api/cafes/{cafe_id}`: Retrieve information about a café.
- **POST** `/api/cafes`: Create a new café.
- **PUT** `/api/cafes/{cafe_id}`: Update a café's information (Admin only).

## Menus

- **GET** `/api/cafes/{cafe_id}/menu?category=<category>&is_available=<true/false>`: List menu of a café.s
- **GET** `/api/cafes/{cafe_id}/menu/{item_id}`: Retrieve information about a menu item.
- **POST** `/api/cafes/{cafe_id}/menu`: Add an item to the menu (Admin).
- **PUT** `/api/cafes/{cafe_id}/menu/{item_id}`: Update a menu item (Admin).
- **DELETE** `/api/cafes/{cafe_id}/menu/{item_id}`: Delete a menu item (Admin).

## Search

- **GET** `/api/search?query=<search_query>&category=<category>&is_available=<true/false>&is_open=<true/false>&payment_method=<method>`: Unified search for both items and cafés.

## Users

- **GET** `/api/users`: List Users.
- **GET** `/api/users/{user_id}`: Retrieve a user’s details, including their name, email...
- **POST** `/api/users`: Create a user.
- **PUT** `/api/users/{user_id}`: Update a user's details or roles.

## Orders

- **GET** `/api/orders`: List Orders.
- **POST** `/api/orders`: Place a new order.
- **GET** `/api/orders/{order_id}`: Retrieve order details.
- **PUT** `/api/orders/{order_id}`: Update an order's status (Bénévole/Admin)
- **GET** `/api/users/{user_id}/orders?status=<status>`: Retrieve a user's orders, with status filtering.
- **GET** `/api/cafes/{cafe_id}/orders?status=<status>`: Retrieve a café's orders, with status filtering.

## Auth

- **POST** `/api/auth/login`: Create access and refresh tokens for user.
- **POST** `/api/auth/test-token`: Test if the access token is valid.
- **POST** `/api/auth/refresh`: Refresh token.