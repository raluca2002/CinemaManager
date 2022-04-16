from dataclasses import dataclass
from Domain.entity import Entity


@dataclass
class Film(Entity):
    #  id_film: str
    titlu: str
    an_aparitie: int
    pret_bilet: float
    in_program: bool
