### Algorithme 4.4 ###
from datetime import datetime
from app.models.cafe_model import Cafe, MenuItem

# Recommand foods to all the users based on the time and the most liked foods.
def main(cafe: Cafe) -> list[MenuItem]:
    time_of_the_day: any = any #TODO
    cafe_items: list[MenuItem] = cafe.menu_items

    # Number of items to recommand.
    if len(cafe_items) > 50:
        k: int = len(cafe_items)//2
    else:
        k: int = len(cafe_items)

    # Find the items with the most likes.
    likes: list[int] = []
    for item in cafe_items:
        likes.append(len(item.likes))
    
    most_likes: list[MenuItem] = []
    for _ in range(k):
        max_likes = max(likes)
        index = likes.index(max_likes)
        most_likes.append(cafe_items[index])
        likes.remove(max_likes)

    #TODO Recommand items based on the time of the day. 
    #   Should be done after nutritionist advice.

    return most_likes
