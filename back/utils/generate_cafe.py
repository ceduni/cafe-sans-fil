import json
from app.models.cafe_model import (
    Cafe,
    MenuItem,
    TimeBlock,
    DayHours,
    Location,
    Contact,
    SocialMedia,
    PaymentMethod,
    AdditionalInfo,
    Role,
    StaffMember,
)
from app.services.user_service import UserService
from app.schemas.user_schema import UserUpdate
from datetime import datetime, timedelta
from tqdm import tqdm
import re
import unicodedata
import random

random.seed(42)


async def create_cafes(usernames):
    cafe_menu_items_slug_dict = {}
    cafes_ids = []

    # Load templates
    with open("./utils/templates/cafes_updated.json", "r", encoding="utf-8") as file:
        cafes_data = json.load(file)
    with open("./utils/templates/menu_items.json", "r", encoding="utf-8") as file:
        menu_items_data = json.load(file)

    for index, cafe_info in enumerate(tqdm(cafes_data, desc="Creating cafes")):
        # Make cafesansfil Admin in First Cafe (For Test)
        if index == 0:
            staff = await random_staff_members(
                usernames, cafe_info["name"], testAccounts, first_user_admin=True
            )
        # Don't make cafesansfil a Staff in second and last Cafe (For Test)
        elif index == 1:
            staff = await random_staff_members(
                usernames, cafe_info["name"], testAccounts, exclude_first_user=True
            )
        elif index == len(cafes_data) - 1:
            staff = await random_staff_members(
                usernames, cafe_info["name"], testAccounts, exclude_first_user=True
            )
        # Randomly choose staff
        else:
            staff = await random_staff_members(
                usernames, cafe_info["name"], testAccounts
            )

        is_open, status_message = random_open_status_message()

        # Randomly set in_stock for each menu item
        randomized_menu_items = []
        for item in menu_items_data:
            item_copy = item.copy()
            item_copy["in_stock"] = random.random() < 0.80
            randomized_menu_items.append(MenuItem(**item_copy))

        cafe = Cafe(
            name=cafe_info["name"],
            features=["Order"] if random.random() <= 0.8 else [],
            description=cafe_info["description"],
            image_url=cafe_info["image_url"],
            faculty=cafe_info["faculty"],
            is_open=is_open,
            status_message=status_message,
            opening_hours=random_opening_hours(),
            location=Location(**cafe_info["location"]),
            contact=Contact(**cafe_info["contact"]),
            social_media=[SocialMedia(**media) for media in cafe_info["social_media"]],
            additional_info=random_additional_info(),
            payment_methods=random_payment_methods(),
            staff=staff,
            menu_items=randomized_menu_items,
        )
        await cafe.insert()

        cafe_menu_items_slug_dict[cafe.slug] = cafe.menu_items
        cafes_ids.append(cafe.cafe_id)

    return cafes_ids, cafe_menu_items_slug_dict, cafes_data


def random_open_status_message():
    messages = [
        "Fermé pour la journée",
        "Fermé pour la semaine",
        "De retour dans 1 heure",
        "Temporairement fermé",
        "Fermé pour MIDIRO",
    ]
    is_open = random.random() < 0.7  # chance of is_open
    status_message = random.choice(messages) if not is_open else None
    return is_open, status_message


def random_opening_hours():
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    opening_hours = []

    for day in days:
        # Randomly choose 2 blocks or not
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


def random_payment_methods():
    methods = ["Carte de débit", "Carte de crédit", "Argent comptant"]
    # Randomly choose methods
    selected_methods_count = random.randint(1, len(methods))
    selected_methods = random.sample(methods, selected_methods_count)
    payment_methods = []

    for method in selected_methods:
        minimum = (
            random.randint(3, 8)
            if method in ["Carte de débit", "Carte de crédit"]
            else None
        )
        payment_methods.append(PaymentMethod(method=method, minimum=minimum))
    return payment_methods


async def random_staff_members(
    usernames, cafe_name, testAccounts, first_user_admin=False, exclude_first_user=False
):
    def reformat(text):
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = text.lower()
        slug = re.sub(r"\W+", ".", text)
        slug = slug.strip(".")
        return slug

    staff_members = []
    selected_users = usernames.copy()
    selected_users.remove("7802085")  # Remove cafesansfil from list of selected users
    for username in testAccounts:
        if username in selected_users:
            selected_users.remove(username)

    # Always choose first User cafesansfil as admin (For Test)
    if first_user_admin:
        staff_members.append(StaffMember(username=usernames[0], role=Role.ADMIN))
        selected_users = selected_users[1:]

    # Never choose first User cafesansfil (For Test)
    if exclude_first_user:
        selected_users = selected_users[1:]

    # Randomly choose how many
    num_admins = random.randint(2, 6) - len(staff_members)
    num_volunteers = random.randint(12, 20)
    selected_users = random.sample(selected_users, num_admins + num_volunteers)
    firstAdmin = False
    firstVolunteer = False

    for username in selected_users[:num_admins]:
        staff_members.append(StaffMember(username=username, role=Role.ADMIN))
        if username in testAccounts:
            raise ValueError(f"Username {username} is already in testAccounts")
        if firstAdmin is False and username not in testAccounts:
            await UserService.update_user(
                username,
                UserUpdate(email="admin." + reformat(cafe_name) + "@umontreal.ca"),
            )
            firstAdmin = True
            testAccounts.append(username)

    for username in selected_users[num_admins:]:
        staff_members.append(StaffMember(username=username, role=Role.VOLUNTEER))
        if username in testAccounts:
            raise ValueError(f"Username {username} is already in testAccounts")
        if firstVolunteer is False and username not in testAccounts:
            await UserService.update_user(
                username,
                UserUpdate(email="benevole." + reformat(cafe_name) + "@umontreal.ca"),
            )
            firstVolunteer = True
            testAccounts.append(username)

    return staff_members


def random_additional_info():
    today = datetime.now()
    info_types = [
        "Événement spécial",
        "Fermeture temporaire",
        "Promotion",
        "Atelier",
        "Nouveau produit",
    ]
    additional_infos = []

    # Lower chance of additional info
    if random.random() < 0.50:
        return additional_infos

    # Randomly choose how many
    num_infos = random.randint(0, 2)
    for _ in range(num_infos):
        event_type = random.choice(info_types)
        # Random start date
        start = today + timedelta(days=random.randint(-3, 0))
        end = None  # Always show for Test and Preview

        date_message = today + timedelta(days=random.randint(-1, 7))
        additional_info = AdditionalInfo(
            type=event_type,
            value=(
                f"{event_type} à {date_message.strftime('%d/%m/%Y')}"
                if random.random() > 0.25
                else f"{event_type}"
            ),
            start=start,
            end=end,
        )
        additional_infos.append(additional_info.model_dump())

    return additional_infos
