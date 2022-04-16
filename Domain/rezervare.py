from datetime import date, time
from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Rezervare(Entity):
    #  id_rezervare: str
    id_film: str
    id_card_client: str
    data: date
    ora: time
