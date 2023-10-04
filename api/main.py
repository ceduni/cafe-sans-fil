from fastapi import FastAPI, APIRouter
from models import User

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API du projet Café sans fil!", "version": "0.1"}


# Tout ce qui sera ajouté dans le router api sera préfixé par /api
api = APIRouter(prefix="/api")


@api.get("/hello")
def hello():
    return {"message": "Hello World!"}


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


app.include_router(api)