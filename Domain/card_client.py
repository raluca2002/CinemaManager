from dataclasses import dataclass
from datetime import date

from Domain.entity import Entity


@dataclass()
class CardClient(Entity):
    #  id_client: str
    nume: str
    prenume: str
    CNP: int
    data_nasterii: date
    data_inregistrarii: date
    puncte_acumulate: int
