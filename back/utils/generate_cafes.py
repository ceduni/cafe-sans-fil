import json
from app.models.cafe_model import Cafe, MenuItem, TimeBlock, DayHours, Location, Contact, SocialMedia, PaymentMethod, AdditionalInfo, Role, StaffMember
from datetime import datetime, timedelta
from tqdm import tqdm
import random
random.seed(42)

async def create_cafes(user_ids):
    cafe_menu_items_ids_dict = {}

    # Load real information about cafes and dummy template menu items
    with open("./utils/cafes_udem.json", "r", encoding="utf-8") as file:
        cafes_data = json.load(file)
    with open("./utils/menuitems.json", "r", encoding="utf-8") as file:
        menu_items_data = json.load(file)
        for item in menu_items_data:
            item["is_available"] = random.random() < 0.8

    for cafe_info in tqdm(cafes_data, desc="Creating cafes"):
        cafe = Cafe(
            name=cafe_info["name"],
            description=cafe_info["description"],
            image_url=cafe_info["image_url"],
            faculty=cafe_info["faculty"],
            is_open=random.random() < 0.8,
            opening_hours=generate_random_opening_hours(),
            location=Location(**cafe_info["location"]),
            contact=Contact(**cafe_info["contact"]),
            social_media=[SocialMedia(**media) for media in cafe_info["social_media"]],
            additional_info=generate_random_additional_info(),
            payment_methods=generate_random_payment_methods(),
            staff=generate_staff_members(user_ids),
            menu_items=[MenuItem(**item) for item in menu_items_data]
        )
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
    # Randomly choose how many
    num_admins = random.randint(1, 6)
    num_volunteers = random.randint(12, 20)
    selected_users = random.sample(user_ids, num_admins + num_volunteers)

    for user_id in selected_users[:num_admins]:
        staff_members.append(StaffMember(user_id=user_id, role=Role.ADMIN))
    for user_id in selected_users[num_admins:]:
        staff_members.append(StaffMember(user_id=user_id, role=Role.VOLUNTEER))
    return staff_members

def generate_random_additional_info():
    today = datetime.now()
    info_types = [
        "Événement spécial", "Fermeture temporaire", "Promotion", "Atelier", "Nouveau produit"
    ]
    additional_infos = []
    
    # Lower chance of additional info
    if random.random() < 0.5:
        return additional_infos

    # Randomly choose how many
    num_infos = random.randint(0, 2)
    for _ in range(num_infos):
        event_type = random.choice(info_types)
        # Random start date within 1 day before or after today, event lasts for 1 day
        start_date = today + timedelta(days=random.randint(-1, 1)) 
        end_date = start_date + timedelta(days=1)

        additional_info = AdditionalInfo(
            type=event_type,
            value=f"{event_type} à {start_date.strftime('%d/%m/%Y')}",
            start=start_date,
            end=end_date
        )
        additional_infos.append(additional_info.model_dump())

    return additional_infos