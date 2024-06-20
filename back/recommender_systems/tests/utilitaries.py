from utils import utilitaries as Utilitaries
from utils import utilitaries as Utilitaries
from app.models.user_model import User
from app.models.cafe_model import Cafe, MenuItem

def test_contains_hight_nutri(item: MenuItem):
    item = MenuItem(**{
        'nutritionnal_informations'
    })
    data = [
        {
            'nutrient': 'lipids',
            'threshold': 3,
            'item': item
        },
        {
            'nutrient': 'proteins',
            'threshold': 10,
            'item': item
        },
    ]

    assert Utilitaries.contains_hight_nutri(**data[0]) == 0
    assert Utilitaries.contains_hight_nutri(**data[1]) == 1