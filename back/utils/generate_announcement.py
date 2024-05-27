from uuid import UUID
from datetime import datetime, timedelta
from random import choice, randint

from app.services.announcement_service import AnnouncementService
from app.schemas.announcement_schema import AnnouncementCreate
from tqdm import tqdm

announcement_templates = [
    ("Promotion de fin de semaine", "Profitez de notre offre spéciale ce weekend avec 20% de réduction sur tous les cafés!"),
    ("Soirée dégustation", "Rejoignez-nous ce samedi pour une soirée dégustation de nos meilleurs crus."),
    ("Offre spéciale", "Toute cette semaine, deux pâtisseries achetées, la troisième offerte!")
]

async def generate_announcements(cafe_ids, user_ids, num_announcements=3):
    for cafe_id in tqdm(cafe_ids, total=len(cafe_ids), desc='Generating announcements'):
        num_to_generate = randint(0, num_announcements)
        for _ in range(num_to_generate):
            title, content = choice(announcement_templates)
            tags = ["promo", "weekend", "special"]
            active_until = datetime.now() + timedelta(days=randint(1, 30))

            announcement_data = AnnouncementCreate(
                cafe_id=cafe_id,
                title=title,
                content=content,
                active_until=active_until,
                tags=tags
            )
            await AnnouncementService.create_announcement(announcement_data)
            
            # # Randomly add likes
            # num_likes = randint(0, 10)  # Random number of likes up to the number of users
            # liked_by_users = choice(user_ids, num_likes, replace=False)
            # for user_id in liked_by_users:
            #     await AnnouncementService.add_like_to_announcement(announcement.announcement_id, user_id)
