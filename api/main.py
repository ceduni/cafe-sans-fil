from fastapi import FastAPI, APIRouter
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
        return {"message": "Utilisateur non trouvé"}
    return {"user": user}


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


@api.get("/cafes/{cafe_id}")
def get_cafe(cafe_id: str):
    return {"message": "Pas encore implémenté"}


app.include_router(api)