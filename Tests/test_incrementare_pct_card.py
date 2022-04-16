from datetime import datetime

from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.undo_redo_service import UndoRedoService
from utiles import clear_file


def test_incrementare_puncte_card_client():
    filename = 'test_card.json'
    clear_file(filename)
    card_client_repository = JsonRepository(filename)
    card_client_validator = CardClientValidator(card_client_repository)
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    added = CardClient("1003", "Popescu", "Ioan", 1791112064557,
                       datetime.strptime("11.12.1979", '%d.%m.%Y').date(),
                       datetime.strptime("20.12.2021", '%d.%m.%Y').date(), 12)
    card_client_repository.create(added)
    added = CardClient("1004", "Birta", "Aurel", 1881016064557,
                       datetime.strptime("16.10.1988", '%d.%m.%Y').date(),
                       datetime.strptime("21.12.2021", '%d.%m.%Y').date(), 0)
    card_client_repository.create(added)
    added = CardClient("1005", "Buga", "Ioana", 2981103064557,
                       datetime.strptime("03.11.2001", '%d.%m.%Y').date(),
                       datetime.strptime("21.12.2021", '%d.%m.%Y').date(), 14)
    card_client_repository.create(added)
    card_client_service.incrementare_puncte_card(datetime.strptime(
        "11.12.1950", '%d.%m.%Y').date(),
                                                 datetime.strptime(
        "11.12.1995", '%d.%m.%Y').date(), 10)
    assert len(card_client_repository.read()) == 3
    assert card_client_repository.read()[0].puncte_acumulate == 22
    assert card_client_repository.read()[1].puncte_acumulate == 10
    assert card_client_repository.read()[2].puncte_acumulate == 14
    card_client_service.incrementare_puncte_card(datetime.strptime(
        "11.12.1999", '%d.%m.%Y').date(),
                                                 datetime.strptime(
        "11.12.2010", '%d.%m.%Y').date(), 20)
    assert len(card_client_repository.read()) == 3
    assert card_client_repository.read()[0].puncte_acumulate == 22
    assert card_client_repository.read()[1].puncte_acumulate == 10
    assert card_client_repository.read()[2].puncte_acumulate == 34
