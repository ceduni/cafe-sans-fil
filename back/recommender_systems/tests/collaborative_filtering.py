from systems import collaborative_filtering as CB
from app.models.user_model import User

def tes_main_1():
    users = []
    user = User()
    assert CB.main(users, user) == []

if __name__ == '__main__':
    tes_main_1()