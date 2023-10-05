from fastapi import FastAPI, APIRouter, HTTPException
from models import User, Cafe

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API du projet Café sans fil!", "version": "0.1"}


# Tout ce qui sera ajouté dans le router api sera préfixé par /api
api = APIRouter(prefix="/api")


@api.get("/hello")
def hello():
    return {"message": "Hello World!"}


# User model


sample_users_db = {
    "3d2e3d2e3d2e3d2e3d2e3d2e": {
        "udem_email": "john.doe@umontreal.ca",
        "first_name": "John",
        "last_name": "Doe",
        "roles": [{
            "cafe_id": "5f897f7d7d6d6d6d6d6d6d6d",
            "role_type": "benevole"
        }]
    },
    "4d2e3d2e3d2e3d2e3d2e3d2e": {
        "udem_email": "steve.jobs@umontreal.ca",
        "first_name": "Steve",
        "last_name": "Jobs",
        "roles": [{
            "cafe_id": "5f897f7d7d6d6d6d6d6d6d6d",
            "role_type": "admin"
        }]
    }
}


@api.get("/users")
def get_users():
    users = []
    for user in sample_users_db:
        users.append(User(**sample_users_db[user]))
    return {"users": users}


@api.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        user = User(**sample_users_db[user_id])
    except KeyError:
        raise HTTPException(status_code=404, detail=f"L'utilisateur {user_id} n'existe pas")
    return {"user": user}


@api.post("/users")
def create_user(user: User):
    return {"message": "Vous ne pouvez pas créer un utilisateur"}


@api.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    return {"message": "Vous ne pouvez pas modifier un utilisateur"}


# Cafe model

def import_cafes_from_json():
    import json
    import os

    json_path = os.path.join(os.path.dirname(__file__), "../data/cafes.json")

    with open(json_path, "r") as f:
        cafes = json.load(f)
    return cafes["cafes"]

sample_cafes_db = import_cafes_from_json()

@api.get("/cafes")
def get_cafes():
    cafes = []
    for cafe in sample_cafes_db:
        cafe["is_open"] = Cafe.Config.schema_extra["example"]["is_open"]
        cafe["opening_hours"] = Cafe.Config.schema_extra["example"]["opening_hours"]
        cafe["payment_methods"] = Cafe.Config.schema_extra["example"]["payment_methods"]
        if "email" not in cafe:
            cafe["email"] = "cafe.sans.email@umontreal.ca"
        cafes.append(Cafe(**cafe))
    return {"cafes": cafes}


@api.get("/cafes?query={cafe_name}")
def search_cafe(cafe_name: str):
    return {"message": f"Ici s'afficheront tous les cafés correspondant à {cafe_name}"}


@api.get("/cafes/{cafe_id}")
def get_single_cafe(cafe_id: str):
    return {"message": f"Ici s'afficheront les informations sur le café {cafe_id}"}


@api.post("/cafes")
def create_cafe(cafe: Cafe):
    return {"message": "Vous ne pouvez pas créer un café"}


@api.put("/cafes/{cafe_id}")
def update_cafe(cafe_id: str, cafe: Cafe):
    return {"message": "Vous ne pouvez pas modifier un café"}


@api.delete("/cafes/{cafe_id}")
def delete_cafe(cafe_id: str):
    return {"message": "Vous ne pouvez pas supprimer un café"}


# Menu model


@api.get("/cafes/{cafe_id}/menu")
def get_menu(cafe_id: str):
    return {"message": f"Ici s'affichera le menu du café {cafe_id}"}


@api.post("/cafes/{cafe_id}/menu")
def add_item_menu(cafe_id: str):
    return {"message": "Vous ne pouvez pas ajouter un item au menu"}


@api.put("/cafes/{cafe_id}/menu/{item_id}")
def update_item_menu(cafe_id: str, item_id: str):
    return {"message": "Vous ne pouvez pas modifier un item du menu"}


@api.delete("/cafes/{cafe_id}/menu/{item_id}")
def delete_item_menu(cafe_id: str, item_id: str):
    return {"message": "Vous ne pouvez pas supprimer un item du menu"}


@api.get("/items?query={item_name}")
def search_item_across_cafes(item_name: str):
    return {"message": f"Ici s'afficheront tous les cafés qui offrent {item_name}"}


# Order model


@api.post("/cafes/{cafe_id}/orders")
def place_order(cafe_id: str):
    return {"message": "Vous ne pouvez pas commander pour le moment"}


@api.get("/orders/{order_id}")
def get_order(order_id: str):
    return {"message": f"Ici s'afficheront les détails de la commande {order_id}"}


@api.put("/orders/{order_id}")
def update_order(cafe_id: str, order_id: str):
    return {"message": f"Vous ne pouvez pas modifier la commande {order_id}"}


@api.get("/users/{user_id}/orders?status={status}")
def get_user_orders(user_id: str, status: str):
    if status is None:
        return {"message": f"Ici s'afficheront toutes les commandes de l'utilisateur {user_id}"}
    return {"message": f"Ici s'afficheront les commandes de l'utilisateur {user_id} ayant le statut {status}"}


@api.get("/cafes/{cafe_id}/orders?status={status}")
def get_orders(cafe_id: str, status: str):
    if status is None:
        return {"message": f"Ici s'afficheront toutes les commandes du café {cafe_id}"}
    return {"message": f"Ici s'afficheront les commandes du café {cafe_id} ayant le statut {status}"}


app.include_router(api)
