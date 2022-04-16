from typing import List
from Domain.card_client import CardClient
from Repository.repository import Repository


class CardValdiationError(Exception):
    pass


class CardClientValidator:
    def __init__(self, card_client_repository: Repository):
        self.card_client_repository = card_client_repository

    @staticmethod
    def validate(card_client: CardClient, carduri: List[CardClient]) -> None:
        errors = []
        if len(str(card_client.id_entity)) == 0:
            errors.append("ID-ul nu poate fi vid!")
        if len(str(card_client.CNP)) != 13:
            errors.append("CNP-ul trebuie sa aibe exact 13 caractere!")
        if len(errors):
            raise CardValdiationError(errors)

    def puncte_validate(self, id_card_client: str) -> None:
        if self.card_client_repository.read(id_card_client) is None:
            raise CardValdiationError(f"Nu exista nici un card "
                                      f"cu ID-ul {id_card_client} ")
