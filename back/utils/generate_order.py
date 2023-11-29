import re
import unicodedata
from app.models.order_model import OrderedItem, OrderStatus, OrderedItemOption
from app.schemas.order_schema import OrderCreate
from app.services.order_service import OrderService
from datetime import datetime, timedelta
from tqdm import tqdm
import random
random.seed(42)

async def create_orders(user_usernames, cafe_menu_items, cafes_data, is_test=False):
    cafe_items_list = list(cafe_menu_items.items())
    cafes_dict = {slugify(cafe["name"]): cafe for cafe in cafes_data}

    for i in tqdm(range(len(user_usernames)), desc="Creating orders"):
        # Minimum 2 Orders for cafesansfil (For Test)
        minimum = 2 + 1 if i == 0 else 0
        maximum = 4 if is_test else 15
        for index in range(random.randint(minimum, maximum)): 
            user_username = user_usernames[i]
            # First Order is related to first cafe (For Test)
            if index == 0:
                cafe_slug, menu_items = cafe_items_list[0]
            # Second Order is not related to cafesansfil in any way (For Test)
            elif index == 1:
                user_username = random.choice(user_usernames[1:])
                cafe_slug, menu_items = cafe_items_list[-1]
            # Other Orders are random
            else:
                cafe_slug, menu_items = random.choice(cafe_items_list)

            cafe_data = cafes_dict.get(cafe_slug)
            cafe_name = cafe_data["name"]
            cafe_image_url = cafe_data["image_url"]

            items = []
            # Probabilities for [<OrderStatus.PLACED: 'Placée'>, <OrderStatus.READY: 'Prête'>, <OrderStatus.COMPLETED: 'Complétée'>, <OrderStatus.CANCELLED: 'Annulée'>]
            weights = [0.075 , 0.075, 0.80, 0.05]  
            status = random.choices(list(OrderStatus), weights, k=1)[0]
            created_at, updated_at = random_timestamps(status)

            # Random items
            for _ in range(random.randint(1, 5)):
                menu_item = random.choice(menu_items)
                quantity = random.randint(1, 5)
                item_price = menu_item.price
                options = []

                # Random options
                if random.choice([True, False]) and menu_item.options:
                    num_options = random.randint(1, len(menu_item.options))
                    selected_options = random.sample(menu_item.options, num_options)
                    options = [OrderedItemOption(type=opt.type, value=opt.value, fee=opt.fee) for opt in selected_options]

                items.append(OrderedItem(
                    item_name=menu_item.name,
                    item_slug=menu_item.slug, 
                    item_image_url=menu_item.image_url,
                    quantity=quantity, 
                    item_price=item_price,
                    options=options
                ))

            order = OrderCreate(
                cafe_name=cafe_name,
                cafe_slug=cafe_slug,
                cafe_image_url=cafe_image_url,
                items=items
            )

            await OrderService.create_order_test(order, user_username, created_at, updated_at, status)

def random_timestamps(status):
    if status == OrderStatus.PLACED:
        created_at = random_minutes_ago(0, 20)
        updated_at = created_at

    elif status == OrderStatus.READY:
        created_at = random_minutes_ago(0, 60)
        updated_at = created_at

    elif status == OrderStatus.CANCELLED:
        created_at = random_days_ago(1, 30)
        if random.random() <= 0.5:
            updated_at = created_at + timedelta(minutes=random.randint(0, 60))
        else:
            updated_at = created_at + timedelta(minutes=60)

    elif status == OrderStatus.COMPLETED:
        created_at = random_days_ago(1, 30)
        updated_at = created_at + timedelta(minutes=random.randint(5, 60))
    
    return created_at, updated_at

def random_minutes_ago(min_minutes, max_minutes):
    minutes_ago = random.randint(min_minutes, max_minutes)
    return datetime.now() - timedelta(minutes=minutes_ago)

def random_days_ago(start_days_ago, end_days_ago):
    days_ago = random.randint(start_days_ago, end_days_ago)
    return datetime.now() - timedelta(days=days_ago)

def slugify(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    slug = re.sub(r'\W+', '-', text)
    slug = slug.strip('-')
    return slug