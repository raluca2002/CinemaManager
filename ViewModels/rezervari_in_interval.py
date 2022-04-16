from dataclasses import dataclass
from datetime import time


@dataclass
class RezervariInInterval:
    id_entity: str
    id_film: str
    id_card: int
    ora_rezervare: time
