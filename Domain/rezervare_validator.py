from Domain.rezervare import Rezervare
from Repository.repository import Repository


class RezervareValidationError(Exception):
    pass


class RezervareValidator:
    def __init__(self,
                 film_repository: Repository,
                 card_client_repository: Repository):
        self.card_client_repository = card_client_repository
        self.film_repository = film_repository

    def validate(self, rezervare: Rezervare, id_film: str,
                 id_card_client: str) -> None:
        if len(str(rezervare.id_entity)) == 0:
            raise RezervareValidationError("ID-ul nu poate fi vid!")
        if self.film_repository.read(id_film) is None:
            raise RezervareValidationError(f"Nu exista nici "
                                           f"un film cu ID-ul {id_film} ")
        if self.card_client_repository.read(id_card_client) is None:
            raise RezervareValidationError(f"Nu exista nici un "
                                           f"card cu ID-ul {id_card_client}")

    def program_film(self, id_film: str) -> None:
        """
        verifica daca filmul este in program
        :param id_film:
        :return:
        """
        film = self.film_repository.read(id_film)
        if film is None:
            raise RezervareValidationError(f"Nu exista"
                                           f" nici un film cu id-ul {id_film}")
        if film.in_program is False:
            raise RezervareValidationError("Filmul nu este in program!")
