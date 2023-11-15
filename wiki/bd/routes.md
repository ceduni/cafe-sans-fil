# 🌐 Routes (API)

Ce document présente les routes et autorisations de notre API.
  
## Cafés

- **GET** `/api/cafes`: List all cafés. <span style="color:blue">🟠</span>
- **GET** `/api/cafes/{cafe_id}`: Retrieve information about a café. <span style="color:blue">🟠</span>
- **POST** `/api/cafes`: Create a new café.
- **PUT** `/api/cafes/{cafe_id}`: Update a café's information. <span style="color:red">🔴</span> 

## Menus

- **GET** `/api/cafes/{cafe_id}/menu`: List menu of a café. <span style="color:blue">🟠</span>
- **GET** `/api/cafes/{cafe_id}/menu/{item_id}`: Retrieve information about a menu item. <span style="color:blue">🟠</span>
- **POST** `/api/cafes/{cafe_id}/menu`: Add an item to the menu. <span style="color:red">🔴</span>
- **PUT** `/api/cafes/{cafe_id}/menu/{item_id}`: Update a menu item. <span style="color:red">🔴</span>
- **DELETE** `/api/cafes/{cafe_id}/menu/{item_id}`: Delete a menu item. <span style="color:red">🔴</span>

## Search

- **GET** `/api/search?query=<search_query>`: Unified search for both items and cafés. <span style="color:blue">🟠</span>

## Users

- **GET** `/api/users`: List Users.
- **GET** `/api/users/{user_id}`: Retrieve a user’s details, including their name, email...  
- **POST** `/api/users`: Create a user. <span style="color:blue">🟠</span>
- **PUT** `/api/users/{user_id}`: Update a user's details. <span style="color:blue">🔵</span>

## Orders

- **GET** `/api/orders`: List Orders. 
- **POST** `/api/orders`: Place a new order. <span style="color:blue">🔵</span> <span style="color:green">🟢</span> <span style="color:red">🔴</span>
- **GET** `/api/orders/{order_id}`: Retrieve order details. <span style="color:blue">🔵</span> <span style="color:green">🟢</span> <span style="color:red">🔴</span>
- **PUT** `/api/orders/{order_id}`: Update an order's status <span style="color:blue">🔵</span> <span style="color:green">🟢</span> <span style="color:red">🔴</span>
- **GET** `/api/users/{user_id}/orders`: Retrieve a user's orders. <span style="color:blue">🔵</span>
- **GET** `/api/cafes/{cafe_id}/orders`: Retrieve a café's orders. <span style="color:green">🟢</span> <span style="color:red">🔴</span>

## Auth

- **POST** `/api/auth/login`: Create access and refresh tokens for user. <span style="color:blue">🟠</span>
- **POST** `/api/auth/test-token`: Test if the access token is valid.
- **POST** `/api/auth/refresh`: Refresh token.

> **Legend**  
> <span style="color:blue">🟠</span> - Public / Guest (Orange)  
> <span style="color:blue">🔵</span> - Member (Blue)  
> <span style="color:green">🟢</span> - Volunteer (Green)  
> <span style="color:red">🔴</span> - Admin (Red)  