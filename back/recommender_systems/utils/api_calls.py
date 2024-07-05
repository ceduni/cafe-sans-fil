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

    # NEEDS AUTHORIZATION
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
    def get_order(order_id, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/orders/{order_id}')
        response = requests.get(url=endpoint, params=params, json=json_data)
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
    
class UserApi:
    # NEEDS AUTHORIZATION
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
        response = requests.patch(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
class UserRecommenderApi:
    @staticmethod
    def get_user_recommendations(cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/user/{cafe_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_user_recommendations(auth_token, cafe_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/user/{cafe_slug}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
class PublicRecommenderApi:
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
    
class BotRecommenderApi:
    @staticmethod
    def get_bot_recommendations(cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/bot/{cafe_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_bot_recommendations(auth_token, cafe_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/bot/{cafe_slug}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
class CafeRecommenderApi:
    @staticmethod
    def get_cafe_recommendations(cafe_slug, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafe/{cafe_slug}')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_cafe_recommendations(auth_token, cafe_slug, params=None, json_data=None):
        headers = {"Authorization": f"Bearer {auth_token['access_token']}"}
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafe/{cafe_slug}')
        response = requests.put(url=endpoint, params=params, json=json_data, headers=headers)
        r = response.json()
        return r, response.status_code
    
    @staticmethod
    def update_user_cafe_recommendations(user_id, params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', f'/api/recommendations/cafe/{user_id}')
        response = requests.put(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code