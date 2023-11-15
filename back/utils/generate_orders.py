from app.models.order_model import Order, OrderedItem
from app.schemas.order_schema import OrderCreate, OrderedItem, OrderStatus
from datetime import datetime, timedelta
from tqdm import tqdm
import random

async def create_orders(user_ids, cafe_menu_items):
    for _ in tqdm(range(len(user_ids)), desc="Creating orders"):
        # Create multiple orders per user
        for _ in range(random.randint(0, 15)): 
            user_id = random.choice(user_ids)
            cafe_id, menu_items = random.choice(list(cafe_menu_items.items()))

            total_price = 0.0
            order_items = []
            order_timestamp = random_past_date(1, 30)

            # Create multiple items per order
            for _ in range(random.randint(1, 5)):
                menu_item = random.choice(menu_items)
                quantity = random.randint(1, 5)

                item_price = menu_item.price
                total_price += item_price * quantity
                order_items.append(OrderedItem(item_id=menu_item.item_id, quantity=quantity, item_price=item_price))

            order_data = OrderCreate(
                user_id=user_id,
                cafe_id=cafe_id,
                items=order_items,
                total_price=total_price,
                status=random.choice(list(OrderStatus)),
                order_timestamp = order_timestamp,
                completion_time = order_timestamp + timedelta(minutes=random.randint(15, 60))
            )

            order = Order(**order_data.model_dump())
            await order.insert()

def random_past_date(start_days_ago, end_days_ago):
    days_ago = random.randint(start_days_ago, end_days_ago)
    random_date = datetime.now() - timedelta(days=days_ago)
    return random_date
