from app.models.order_model import Order, OrderedItem, OrderStatus, OrderedItemOption
from datetime import datetime, timedelta
from tqdm import tqdm
import random
random.seed(42)

async def create_orders(user_ids, cafe_menu_items):
    for _ in tqdm(range(len(user_ids)), desc="Creating orders"):
        # Radom orders per user
        for _ in range(random.randint(0, 15)): 
            user_id = random.choice(user_ids)
            cafe_id, menu_items = random.choice(list(cafe_menu_items.items()))
            order_items = []
            created_at = random_past_date(1, 30)

            # Random items
            for _ in range(random.randint(1, 5)):
                menu_item = random.choice(menu_items)
                quantity = random.randint(1, 5)
                item_price = menu_item.price
                item_options = []

                # Random options
                if random.choice([True, False]) and menu_item.options:
                    num_options = random.randint(1, len(menu_item.options))
                    selected_options = random.sample(menu_item.options, num_options)
                    item_options = [OrderedItemOption(type=opt.type, value=opt.value, fee=opt.fee) for opt in selected_options]

                order_items.append(OrderedItem(
                    item_id=menu_item.item_id, 
                    quantity=quantity, 
                    item_price=item_price,
                    options=item_options
                ))

            order = Order(
                user_id=user_id,
                cafe_id=cafe_id,
                items=order_items,
                status=random.choice(list(OrderStatus)),
                created_at = created_at,
                updated_at = created_at + timedelta(minutes=random.randint(15, 60))
            )
            await order.insert()

def random_past_date(start_days_ago, end_days_ago):
    days_ago = random.randint(start_days_ago, end_days_ago)
    random_date = datetime.now() - timedelta(days=days_ago)
    return random_date
