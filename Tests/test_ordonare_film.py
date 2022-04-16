from datetime import datetime
from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from utiles import clear_file


def test_ordonare_film():
    filename1 = 'test_film.json'
    filename2 = 'test_rezervare.json'
    filename3 = 'test_card.json'
    clear_file(filename1)
    clear_file(filename2)
    clear_file(filename3)
    film_repository = JsonRepository(filename1)
    card_client_repository = JsonRepository(filename2)
    rezervare_repository = JsonRepository(filename3)
    rezervare_validator = RezervareValidator(film_repository,
                                             card_client_repository)
    undo_redo_service = UndoRedoService()
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    added = Film("1008", "Cel mai bogat om", 1980, 15.50, True)
    film_repository.create(added)
    added = Film("1009", "Pistruiatul", 1973, 19.50, True)
    film_repository.create(added)
    added = Film("1010", "Fulgi de hartie", 1979, 20.00, True)
    film_repository.create(added)
    added = CardClient("1006", "Buga", "Ioana", 2981103064557,
                       datetime.strptime("03.11.1998", '%d.%m.%Y').date(),
                       datetime.strptime("21.12.2021", '%d.%m.%Y').date(), 14)
    card_client_repository.create(added)
    added = Rezervare("1002", "1009", "1006",
                      datetime.strptime("12.11.2021", '%d.%m.%Y').date(),
                      datetime.strptime("12.22", '%H.%M').time())
    rezervare_repository.create(added)
    added = Rezervare("1003", "1009", "1006",
                      datetime.strptime("12.11.2021", '%d.%m.%Y').date(),
                      datetime.strptime("22.32", '%H.%M').time())
    rezervare_repository.create(added)
    added = Rezervare("1004", "1009", "1006",
                      datetime.strptime("12.11.2021", '%d.%m.%Y').date(),
                      datetime.strptime("12.52", '%H.%M').time())
    rezervare_repository.create(added)
    added = Rezervare("1005", "1010", "1006",
                      datetime.strptime("12.11.2021", '%d.%m.%Y').date(),
                      datetime.strptime("14.22", '%H.%M').time())
    rezervare_repository.create(added)
    filme = rezervare_service.ordoneaza_filme_dupa_nr_rez()
    assert len(filme) == 3
    assert filme[0].titlu == "Pistruiatul"
    assert filme[1].titlu == "Fulgi de hartie"
    assert filme[2].titlu == "Cel mai bogat om"
