from app.models.order_model import Order, OrderedItem, OrderStatus, OrderedItemOption
from datetime import datetime, timedelta
from tqdm import tqdm
import random
random.seed(42)

async def create_orders(user_ids, cafe_menu_items, is_test=False):
    cafe_items_list = list(cafe_menu_items.items())

    for i in tqdm(range(len(user_ids)), desc="Creating orders"):
        # Minimum 2 Orders for cafesansfil (For Test)
        minimum = 2 + 1 if i == 0 else 0
        maximum = 4 if is_test else 15
        for index in range(random.randint(minimum, maximum)): 
            user_id = user_ids[i]
            # First Order is related to first cafe (For Test)
            if index == 0:
                cafe_id, menu_items = cafe_items_list[0]
            # Second Order is not related to cafesansfil in any way (For Test)
            elif index == 1:
                user_id = random.choice(user_ids[1:])
                cafe_id, menu_items = cafe_items_list[-1]
            # Other Orders are random
            else:
                cafe_id, menu_items = random.choice(cafe_items_list)

            items = []
            status = random.choice(list(OrderStatus))
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
                    item_id=menu_item.item_id, 
                    quantity=quantity, 
                    item_price=item_price,
                    options=options
                ))

            order = Order(
                user_id=user_id,
                cafe_id=cafe_id,
                items=items,
                status=status,
                created_at = created_at,
                updated_at = updated_at
            )
            await order.insert()

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