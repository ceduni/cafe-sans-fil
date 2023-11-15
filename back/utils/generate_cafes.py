import json
from app.models.cafe_model import Cafe
from app.schemas.cafe_schema import CafeCreate, MenuItemCreate, TimeBlock, DayHours, Contact, SocialMedia, PaymentMethod, StaffMember
from tqdm import tqdm
import random

async def create_cafes(user_ids, fake):
    cafe_menu_items_ids_dict = {}

    # Load real information about cafes
    with open("./utils/cafes_udem.json", "r", encoding="utf-8") as file:
        cafes_data = json.load(file)

    # Load dummy template for menu items
    with open("./utils/menuitems.json", "r", encoding="utf-8") as file:
        menu_items_data = json.load(file)
        for item in menu_items_data:
            item["image_url"] = fake.image_url(width=640, height=480)
            item["is_available"] = fake.boolean()
            item["additional_info_menu"] = generate_random_additional_info()

    for cafe_info in tqdm(cafes_data, desc="Creating cafes"):
        cafe_data = CafeCreate(
            name=cafe_info["name"],
            description=cafe_info["description"],
            image_url=fake.image_url(width=640, height=480),
            faculty=cafe_info["faculty"],
            location=cafe_info["location"],
            is_open=fake.boolean(),
            opening_hours=generate_random_opening_hours(),
            contact=Contact(**cafe_info["contact"]),
            social_media=[SocialMedia(**media) for media in cafe_info["social_media"]],
            payment_methods=generate_random_payment_methods(),
            staff=generate_staff_members(user_ids),
            menu_items=[MenuItemCreate(**item) for item in menu_items_data],
            additional_info_cafe=generate_random_additional_info_cafe(fake)
        )
        
        cafe = Cafe(**cafe_data.model_dump())
        await cafe.insert()
        cafe_menu_items_ids_dict[cafe.cafe_id] = cafe.menu_items

    return cafe_menu_items_ids_dict

def generate_random_opening_hours():
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    opening_hours = []

    for day in days:
        # Randomly choose if 2 blocks or not
        has_break = random.choice([True, False])
        morning_start_hour = random.randint(8, 10)
        morning_start = f"{morning_start_hour:02d}:00"

        if has_break:
            morning_end_hour = random.randint(11, 13)
            morning_end = f"{morning_end_hour:02d}:00"
            afternoon_start_hour = morning_end_hour + 1
            afternoon_start = f"{afternoon_start_hour:02d}:00"
        else:
            morning_end = afternoon_start = "17:00"

        afternoon_end_hour = random.randint(16, 18)
        afternoon_end = f"{afternoon_end_hour:02d}:00"

        blocks = [TimeBlock(start=morning_start, end=morning_end)]
        if has_break:
            blocks.append(TimeBlock(start=afternoon_start, end=afternoon_end))    
        opening_hours.append(DayHours(day=day, blocks=blocks))

    return opening_hours

def generate_random_payment_methods():
    methods = ["Carte de débit", "Carte de crédit", "Espèces", "Chèque"]
    # Randomly choose methods
    selected_methods_count = random.randint(1, len(methods))
    selected_methods = random.sample(methods, selected_methods_count)

    payment_methods = []
    for method in selected_methods:
        minimum = round(random.uniform(0.0, 7.0), 2) if method in ["Carte de débit", "Carte de crédit"] else None
        payment_methods.append(PaymentMethod(method=method, minimum=minimum))
    return payment_methods

def generate_staff_members(user_ids):
    staff_members = []
    num_admins = random.randint(1, 6)
    num_volunteers = random.randint(12, 20)
    selected_users = random.sample(user_ids, num_admins + num_volunteers)

    for user_id in selected_users[:num_admins]:
        staff_members.append(StaffMember(user_id=user_id, role="admin"))
    for user_id in selected_users[num_admins:]:
        staff_members.append(StaffMember(user_id=user_id, role="volunteer"))
    return staff_members

def generate_random_additional_info():
    info_options = [
        {"key": "Size", "value": "Small, Medium, Large"},
        {"key": "Topping", "value": "Chocolate, Caramel, Vanilla, Hazelnut, Maple"},
        {"key": "", "value": ""},
        {"key": "", "value": ""},
        {"key": "", "value": ""}
    ]
    return [random.choice(info_options)]

def generate_random_additional_info_cafe(fake):
    info_options = [
        {"key": "Événement spécial", "value": fake.sentence(nb_words=6)},
        {"key": "Fermeture", "value": fake.sentence(nb_words=4)},
        {"key": "Autre", "value": fake.sentence(nb_words=5)},
        {"key": "", "value": ""},
        {"key": "", "value": ""},
        {"key": "", "value": ""}
    ]
    return [random.choice(info_options)]