"""
Interaction seeder module.
"""

import random
from datetime import UTC, datetime, timedelta, timezone
from typing import List, Optional

from tqdm import tqdm
from uuid import uuid4
from app.notification.models import (
    NotificationMessage,
    NotificationStatus,
    Action,
    NotificationType,
    ActionType,
)
from app.user.models import User
from app.user.service import UserService

random.seed(42)

titles = {
    NotificationType.INFO: ["Bienvenue sur la plateforme !", "Info du jour", "Conseil étudiant"],
    NotificationType.PROMO: ["Offre au café étudiant !", "Promotion spéciale pour les membres", "Café gratuit ? Oui !"],
    NotificationType.ALERT: ["Salle de réunion déplacée", "Interruption de service", "Modification de dernière minute"],
    NotificationType.UPDATE: ["Nouvelle fonctionnalité disponible", "Améliorations du système", "Mise à jour des conditions d’utilisation"],
    NotificationType.EVENT: ["Soirée jeux ce vendredi !", "Atelier CV et LinkedIn", "Café débat : thème éco-campus"]
}

messages = {
    NotificationType.INFO: [
        "Merci de vous être inscrit·e !",
        "Voici comment profiter au mieux des services du campus.",
        "Le Café étudiant est ouvert de 8h à 18h aujourd'hui."
    ],
    NotificationType.PROMO: [
        "Un café offert pour tout muffin acheté ce lundi.",
        "-20% sur les boissons chaudes cette semaine.",
        "Participez à notre jeu concours pour gagner un brunch gratuit !"
    ],
    NotificationType.ALERT: [
        "La réunion prévue en salle B est déplacée en salle D.",
        "La plateforme sera inaccessible entre 22h et 23h pour maintenance.",
        "L'événement 'Soirée jeux' commencera à 19h au lieu de 18h."
    ],
    NotificationType.UPDATE: [
        "Découvrez notre nouvelle section Événements étudiants.",
        "La navigation a été améliorée pour plus de fluidité.",
        "Nos conditions générales ont été mises à jour."
    ],
    NotificationType.EVENT: [
        "Rejoignez-nous vendredi pour une soirée conviviale dès 18h.",
        "Inscrivez-vous à l’atelier du jeudi pour booster votre CV.",
        "Participez au débat autour des initiatives écoresponsables du campus."
    ]
}

def generate_notification(ntype: NotificationType):
    title = random.choice(titles[ntype])
    message = random.choice(messages[ntype])
    return {
        "title": title,
        "message": message,
        "type": ntype.value,
        "action": {
            "type": ActionType.LINK.value,
            "url": f"https://etu.univ.fr/redirect/{uuid4().hex[:6]}"
        } if random.random() < 0.7 else None,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))).isoformat()
    }
    

class NotificationSeeder:
    """Notification seeder class."""

    def __init__(self):
        """Initializes the NotificationSeeder."""
        self.notificationMessages: List = []
        self.notificationStatuses: List = []
        self.users: List[User] = []
        

    async def seed_notifications(self, num_notifications: int = 100, num_notifications_per_user:  Optional[List[int]] = None):
        """Seed notifications."""
        self.users = await UserService.get_all()
        
        if num_notifications_per_user is None:
            num_notifications_per_user = [5, 10]
        
        for _ in tqdm(range(num_notifications), desc="Notification messages"):
            notification_type = random.choices(
                [NotificationType.INFO, NotificationType.EVENT, NotificationType.PROMO, NotificationType.ALERT],
                weights=[0.3, 0.4, 0.3, 0.1],
                k=1
            )[0]
            notification = generate_notification(notification_type)
            self.notificationMessages.append(NotificationMessage(
                title=notification["title"],
                message=notification["message"],
                type=notification["type"]
            ))

        result = await NotificationMessage.insert_many(self.notificationMessages)
        notification_ids = result.inserted_ids
        
        # Get random subset of users
        users = random.sample(
            self.users,
            k=random.randint(
                int(len(self.users) * 0.2), int(len(self.users) * 0.6)
            ),
        )
        
        for user in tqdm(users, desc="Notification status"):
            num_user_notifications = random.randint(*num_notifications_per_user)
            selected_ids = random.sample(notification_ids, k=min(num_user_notifications, len(notification_ids)))
             
            for message_id in selected_ids:
                self.notificationStatuses.append(
                    NotificationStatus(
                        user_id=user.id,
                        message_id=message_id,
                        read=random.choice([True, False]),
                        delivered_at=self._random_date(),
                    )
                )
                
        await NotificationStatus.insert_many(self.notificationStatuses)


    def _random_date(self) -> datetime:
        """Generate random date within last 6 months."""
        return datetime.now(UTC) - timedelta(
            days=random.randint(0, 180), hours=random.randint(0, 23)
        )
