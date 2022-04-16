from datetime import date
from typing import List
from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Domain.update_operation_loop import UpdateOperationLoop
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.orderedcards import OrderedCards


class CardClientService:
    def __init__(self, card_client_repository: Repository,
                 card_client_validator: CardClientValidator,
                 undo_redo_service: UndoRedoService):
        self.card_client_repository = card_client_repository
        self.card_client_validator = card_client_validator
        self.undo_redo_service = undo_redo_service

    def add_card(self, id_client: str, nume: str,
                 prenume: str, cnp: int, data_nasterii: date,
                 data_inregistrarii: date, puncte_acumulate: int) -> None:
        """
        adaugarea unui card
        :param id_client:
        :param nume:
        :param prenume:
        :param cnp:
        :param data_nasterii:
        :param data_inregistrarii:
        :param puncte_acumulate:
        :return:
        """
        card = CardClient(id_client, nume, prenume, cnp,
                          data_nasterii, data_inregistrarii, puncte_acumulate)
        carduri = self.get_all_card()
        self.card_client_validator.validate(card, carduri)
        self.card_client_repository.create(card)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.card_client_repository, card)
        self.undo_redo_service.add_to_undo(add_operation)

    def get_all_card(self) -> List[CardClient]:
        """
        preia toate entitatiile
        :return:
        """
        return self.card_client_repository.read()

    def update_card(self, id_client: str, nume_new: str, prenume_new: str,
                    cnp_new: int,
                    data_nasterii_new: date, data_inregistrarii_new: date,
                    puncte_acumulate_new: int) -> None:
        """
        actualizarea unui card
        :param id_client:
        :param nume_new:
        :param prenume_new:
        :param cnp_new:
        :param data_nasterii_new:
        :param data_inregistrarii_new:
        :param puncte_acumulate_new:
        :return:
        """
        card_before = self.card_client_repository.read(id_client)
        card = CardClient(id_client, nume_new, prenume_new, cnp_new,
                          data_nasterii_new, data_inregistrarii_new,
                          puncte_acumulate_new)
        carduri = self.get_all_card()
        self.card_client_validator.validate(card, carduri)
        self.card_client_repository.update(card)

        self.undo_redo_service.clear_redo()
        updated_operation = UpdateOperation(self.card_client_repository, card,
                                            card_before)
        self.undo_redo_service.add_to_undo(updated_operation)

    def delete_card(self, id_client: str) -> None:
        """
        Stergerea unui film
        :param id_client: str
        :return:
        """
        self.card_client_repository.delete(id_client)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.card_client_repository,
                                           self.card_client_repository.read(
                                               id_client))
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_puncte_card(self, id_card) -> int:
        """
        determina punctele de pe cardul cu id-ul id_card
        :param id_card:
        :return:
        """
        card_client = self.card_client_repository.read(id_card)
        return card_client.puncte_acumulate

    def ord_desc_dupa_nr_puncte(self) -> List[OrderedCards]:
        """
        ordoneaza cardurile client dupa punctele acumulate
        :return:
        """
        carduri = self.get_all_card()
        ord_carduri = map(
            lambda puncte: OrderedCards(puncte.nume,
                                        puncte.prenume,
                                        puncte.puncte_acumulate), carduri)
        return sorted(ord_carduri, key=lambda x: x.points, reverse=True)

    def incrementare_puncte_card(self, data_start: date, data_stop: date,
                                 val: int) -> None:
        """
        :param data_start:
        :param data_stop:
        :param val:
        :return:
        """
        card_clienti = self.get_all_card()
        for card_client in card_clienti:
            if data_start <= card_client.data_nasterii <= data_stop:
                card_client.puncte_acumulate += val
                self.card_client_repository.update(card_client)

        self.undo_redo_service.clear_redo()
        upd_operation = UpdateOperationLoop(self.card_client_repository,
                                            card_clienti,
                                            self.card_client_repository.read())
        self.undo_redo_service.add_to_undo(upd_operation)
