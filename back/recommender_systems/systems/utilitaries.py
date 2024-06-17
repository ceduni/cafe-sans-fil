# Ce fichier contient le code des algorithmes de la section 2 du document
#   "Logique" du wiki.

from back.app.models.cafe_model import MenuItem, Cafe
from back.app.models.user_model import User
from back.app.models.order_model import Order, OrderedItem
from back.app.services.cafe_service import CafeService

# This method takes the actual user and the cafe as parameters and return
#   a list of items not yet consummed by the user.
async def meal_not_consumed(cafe: Cafe, user: User) -> list[MenuItem]:
    cafe_slug = cafe.slug
    order_history: list[Order] = user.order_history
    oredered_items_slugs: list[str] = []
    for order in order_history:
        oredered_items: list[OrderedItem] = order.items
        for item in oredered_items:
            oredered_items_slugs.append(item.item_slug)
    
    meal_not_consumed: list[MenuItem] = []
    for item_slug in oredered_items_slugs:
        item = await CafeService.retrieve_menu_item(cafe_slug, item_slug)
        if item != None:
            meal_not_consumed.append(item)

    return meal_not_consumed

'''
def intersection(A: list, B: list) -> list:
    res = []
    for elem in A:
        if elem in B:
            res.append(elem)
    return res

### Test the code with each similarity and choose the best one.
def jaccard(A: list, B: list):
    A.extend(B)
    inter = intersection(A, B)
    return len(inter) / len(A)

def cosine_similarity(x,y):
    return

def pearson_correlation(x,y):
    return
'''