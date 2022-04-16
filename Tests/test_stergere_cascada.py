from datetime import datetime
from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from utiles import clear_file


def test_stergere_in_cascada():
    filename_film = 'test_film.json'
    filename_card = 'test_card.json'
    filename_rezervare = 'test_rezervare.json'
    clear_file(filename_film)
    clear_file(filename_card)
    clear_file(filename_rezervare)
    card_client_repository = JsonRepository(filename_card)
    film_repository = JsonRepository(filename_film)
    rezervare_repository = JsonRepository(filename_rezervare)
    rezervare_validator = RezervareValidator(film_repository,
                                             card_client_repository)
    undo_redo_service = UndoRedoService()
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    added = Film("1005", "Omul", 1971, 24.50, True)
    film_repository.create(added)
    added = Film("1006", "Frica", 1969, 29.50, False)
    film_repository.create(added)
    added = Film("1009", "Minciuna", 1979, 20.00, True)
    film_repository.create(added)
    added = CardClient("1006", "Buga", "Ioana", 2981103064557,
                       datetime.strptime("03.11.1998", '%d.%m.%Y').date(),
                       datetime.strptime("21.12.2021", '%d.%m.%Y').date(), 14)
    card_client_repository.create(added)
    added = Rezervare("1002", "1009", "1006",
                      datetime.strptime("13.11.2021", '%d.%m.%Y').date(),
                      datetime.strptime("12.22", '%H.%M').time())
    rezervare_repository.create(added)
    added = Rezervare("1003", "1005", "1006",
                      datetime.strptime("13.12.2021", '%d.%m.%Y').date(),
                      datetime.strptime("22.32", '%H.%M').time())
    rezervare_repository.create(added)
    added = Rezervare("1004", "1009", "1006",
                      datetime.strptime("14.12.2021", '%d.%m.%Y').date(),
                      datetime.strptime("12.52", '%H.%M').time())
    rezervare_repository.create(added)
    added = Rezervare("1005", "1006", "1006",
                      datetime.strptime("16.12.2021", '%d.%m.%Y').date(),
                      datetime.strptime("14.22", '%H.%M').time())
    rezervare_repository.create(added)
    assert len(rezervare_repository.read()) == 4
    film_repository.delete("1005")
    rezervare_service.stergere_in_cascada_film("1005")
    assert rezervare_repository.read("1003") is None
    assert len(rezervare_repository.read()) == 3
    card_client_repository.delete("1006")
    rezervare_service.stergere_in_cascada_card_client("1006")
    assert len(rezervare_repository.read()) == 0
