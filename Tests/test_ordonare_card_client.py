from datetime import datetime
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.undo_redo_service import UndoRedoService
from utiles import clear_file


def test_ordonare_card_client():
    filename = 'test_card.json'
    clear_file(filename)
    card_client_repository = JsonRepository(filename)
    card_client_validator = CardClientValidator(card_client_repository)
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    added = CardClient("1004", "Bostan", "Ioan", 1791112064557,
                       datetime.strptime("11.12.1979", '%d.%m.%Y').date(),
                       datetime.strptime("20.12.2021", '%d.%m.%Y').date(), 12)
    card_client_repository.create(added)
    added = CardClient("1005", "Enea", "Aurel", 1881016064557,
                       datetime.strptime("16.10.1988", '%d.%m.%Y').date(),
                       datetime.strptime("21.12.2021", '%d.%m.%Y').date(), 0)
    card_client_repository.create(added)
    added = CardClient("1006", "Baciu", "Ioana", 2981103064557,
                       datetime.strptime("03.11.1998", '%d.%m.%Y').date(),
                       datetime.strptime("21.12.2021", '%d.%m.%Y').date(), 14)
    card_client_repository.create(added)
    carduri = card_client_service.ord_desc_dupa_nr_puncte()
    assert len(carduri) == 3
    assert carduri[0].nume_card == "Baciu"
    assert carduri[1].nume_card == "Bostan"
    assert carduri[2].nume_card == "Enea"
