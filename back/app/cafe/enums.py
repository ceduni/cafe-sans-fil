from enum import Enum


class Feature(str, Enum):
    ORDER = "Order"


class Days(str, Enum):
    MONDAY = "Lundi"
    TUESDAY = "Mardi"
    WEDNESDAY = "Mercredi"
    THURSDAY = "Jeudi"
    FRIDAY = "Vendredi"
    SATURDAY = "Samedi"
    SUNDAY = "Dimanche"


class Role(str, Enum):
    VOLUNTEER = "Bénévole"
    ADMIN = "Admin"
