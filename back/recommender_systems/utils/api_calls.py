import requests
from urllib.parse import urljoin

class AuthApi:
    @staticmethod
    def auth_login():
        login_data = {
            "username": "7802085",
            "password": "Cafepass1",
        }
        endpoint = urljoin('http://127.0.0.1:8000', "/api/auth/login")
        response = requests.post(url=endpoint, data=login_data)
        return response.json()

class OrderApi:
    @staticmethod
    def get_orders(auth_token, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', '/api/orders')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def get_user_orders(auth_token, username, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/users/{username}/orders')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def get_order(auth_token, order_id, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/orders/{order_id}')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
class CafeApi:
    @staticmethod
    def get_cafes(auth_token, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', '/api/cafes')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def get_all_items(cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/cafes/{cafe_slug}/menu')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def get_item(auth_token ,cafe_slug, item_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/cafes/{cafe_slug}/menu/{item_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_item(auth_token, cafe_slug, item_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/cafes/{cafe_slug}/menu/{item_slug}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_cafe(auth_token, cafe_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/cafes/{cafe_slug}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
class UserApi:
    @staticmethod
    def get_user(auth_token, username, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/users/{username}')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code

    @staticmethod
    def get_users(auth_token, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', '/api/users')
        response = requests.get(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_user(auth_token, username, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/users/{username}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
class RecommendationsApi:
    @staticmethod
    def get_cafe(cafe_slug):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafe_for_recommendation/{cafe_slug}')
        response = requests.get(url=endpoint)
        r = response.json()
        return r, response.status_code
    
    def get_item(item_id: str):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/item/{item_id}')
        response = requests.get(url=endpoint)
        r = response.json()
        return r, response.status_code

    @staticmethod
    def update_items_health_score(auth_token, item_id, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/item/{item_id}')
        response = requests.put(url=endpoint, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_cafe_health_score(auth_token, cafe_slug, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafe/health_score/{cafe_slug}')
        response = requests.put(url=endpoint, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    #--------------------------------------
    #          Public recommendations
    #--------------------------------------

    @staticmethod
    def get_public_recommendations(cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/public/{cafe_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_public_recommendations(auth_token, cafe_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/public/{cafe_slug}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    #---------------------------------------
    #          user's recommendation
    #---------------------------------------

    @staticmethod
    def get_user(user_id):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/user/{user_id}')
        response = requests.get(url=endpoint)
        r = response.json()
        return r, response.status_code

    @staticmethod
    def get_user_personnal_recommendations(user_id, cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/user/{user_id}/{cafe_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_user_personnal_recommendations(auth_token, user_id, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/user/{user_id}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def get_user_cafe_recommendations(user_id, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafes_recommendations/{user_id}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_user_cafe_recommendations(auth_token, user_id, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafes_recommendations/{user_id}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    #---------------------------------------
    #          Bot recommendation
    #---------------------------------------

    @staticmethod
    def get_bot_recommendations(cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/bot/{cafe_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code