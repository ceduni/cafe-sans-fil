import requests
from urllib.parse import urljoin
class CafeApi:
    @staticmethod
    def get_cafes(params=None, json_data=None):
        endpoint = urljoin('http://127.0.0.1:8000', '/api/cafes')
        response = requests.get(url=endpoint, params=params, json=json_data)
        r = response.json()
        return r, response.status_code
    
