from uuid import UUID
from datetime import datetime, timedelta
from random import choice, randint, sample
from tqdm import tqdm

from app.services.event_service import EventService
from app.schemas.event_schema import EventCreate

event_templates = [
    ("Nuit de musique live", "Venez vivre une expérience unique avec notre soirée musique live ce vendredi!"),
    ("Soirée cinéma", "Rejoignez-nous pour une projection exclusive d'un classique du cinéma sous les étoiles."),
    ("Dégustation de vins", "Explorez notre sélection exclusive de vins lors de notre prochaine soirée dégustation.")
]

image_urls = [
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fditto.tv%2Fwp-content%2Fuploads%2F2020%2F03%2FAdobeStock_166872827-2048x1176.jpeg&f=1&nofb=1&ipt=3d4c249727ebf6eadfda0a36161d0bf4551d5d8a5304cdc06a38ec55af0e1e60&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fkuleanaeducation.weebly.com%2Fuploads%2F1%2F7%2F1%2F0%2F17103526%2Fs142233709560776753_p52_i1_w640.jpeg&f=1&nofb=1&ipt=5a2e62c2d22a9a4eec4c503ec473fb19ceddb84853e9b20ef3ddf81e42afa231&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages5.alphacoders.com%2F386%2F386646.jpg&f=1&nofb=1&ipt=a33b13d597e6d65481fb906a24ba9800c244eb0406ca1d154d0c8f344875411d&ipo=imagesg"
]

async def generate_events(cafe_ids, user_ids, num_events=3):
    for cafe_id in tqdm(cafe_ids, total=len(cafe_ids), desc="Generating events"):
        num_to_generate = randint(0, num_events)
        for _ in range(num_to_generate):
            title, description = choice(event_templates)
            start_date = datetime.now() + timedelta(days=randint(1, 30))
            end_date = start_date + timedelta(hours=randint(2, 6))  # Events last between 2 to 6 hours
            image_url = choice(image_urls)

            event_data = EventCreate(
                cafe_id=cafe_id,
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                image_url=image_url
            )
            event = await EventService.create_event(event_data)
            
            # Randomly add attendees
            num_attendees = randint(0, 12)  # Random number of attendees up to the number of users
            attendees = sample(user_ids, num_attendees)
            for user_id in attendees:
                await EventService.add_attendee_to_event(event.event_id, user_id)
            
            # Randomly add supporters
            num_supporters = randint(0, 12)  # Random number of supporters up to the number of users
            supporters = sample(user_ids, num_supporters)
            for user_id in supporters:
                await EventService.add_supporter_to_event(event.event_id, user_id)
