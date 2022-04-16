from datetime import datetime
from Domain.card_client_validator import CardClientValidator
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from utiles import clear_file


def test_undo_redo():
    film_file = 'test_film.json'
    card_file = 'test_card.json'
    rezervre_file = 'test_rezervare.json'
    clear_file(film_file)
    clear_file(card_file)
    clear_file(rezervre_file)
    film_repository = JsonRepository(film_file)
    card_client_repository = JsonRepository(card_file)
    rezervare_repository = JsonRepository(rezervre_file)
    rezervare_validator = RezervareValidator(film_repository,
                                             card_client_repository)
    undo_redo_service = UndoRedoService()
    film_validator = FilmValidator()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)
    card_client_validator = CardClientValidator(card_client_repository)
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    film_service.add_film("1005", "Omul", 1971, 24.50, True)
    film_service.add_film("1006", "Fulgi de hartie", 1969, 29.50, True)
    film_service.add_film("1009", "Mintea", 1979, 20.00, True)
    assert len(film_repository.read()) == 3
    undo_redo_service.do_undo()
    undo_redo_service.do_undo()
    assert len(film_repository.read()) == 1
    undo_redo_service.de_redo()
    undo_redo_service.de_redo()
    undo_redo_service.de_redo()
    assert len(film_repository.read()) == 3

    card_client_service.add_card("1006", "Cioban", "Alin", 2981103064557,
                                 datetime.strptime(
                                     "03.11.1998", '%d.%m.%Y').date(),
                                 datetime.strptime(
                                     "21.12.2021", '%d.%m.%Y').date(), 14)
    assert len(card_client_repository.read()) == 1
    card_client_service.update_card("1006", "Enea", "Ioana", 5130601060889,
                                    datetime.strptime(
                                        "01.06.2013", '%d.%m.%Y').date(),
                                    datetime.strptime(
                                        "12.12.2021", '%d.%m.%Y').date(), 0)

    assert card_client_repository.read("1006").nume == "Enea"
    assert card_client_repository.read("1006").prenume == "Ioana"
    assert card_client_repository.read("1006").puncte_acumulate == 0
    undo_redo_service.do_undo()
    assert card_client_repository.read("1006").nume == "Cioban"
    assert card_client_repository.read("1006").prenume == "Alin"
    assert card_client_repository.read("1006").puncte_acumulate == 14

    rezervare_service.add_rezervare("1002", "1009", "1006",
                                    datetime.strptime(
                                        "13.11.2021", '%d.%m.%Y').date(),
                                    datetime.strptime(
                                        "12.22", '%H.%M').time())
    rezervare_service.add_rezervare("1003", "1005", "1006",
                                    datetime.strptime(
                                        "13.12.2021", '%d.%m.%Y').date(),
                                    datetime.strptime(
                                        "22.32", '%H.%M').time())

    rezervare_service.add_rezervare("1004", "1009", "1006",
                                    datetime.strptime(
                                        "14.12.2021", '%d.%m.%Y').date(),
                                    datetime.strptime(
                                        "12.52", '%H.%M').time())

    rezervare_service.add_rezervare("1005", "1006", "1006",
                                    datetime.strptime(
                                        "16.12.2021", '%d.%m.%Y').date(),
                                    datetime.strptime("14.22", '%H.%M').time())

    assert len(rezervare_repository.read()) == 4
    rezervare_service.stergere_rezervari_interval_zile(datetime.strptime(
        "01.10.1900", '%d.%m.%Y').date(),
                                                       datetime.strptime(
        "30.11.2022", '%d.%m.%Y').date())
    assert len(rezervare_repository.read()) == 0
    undo_redo_service.do_undo()
    assert len(rezervare_repository.read()) == 4
    undo_redo_service.de_redo()
    assert len(rezervare_repository.read()) == 0
    undo_redo_service.do_undo()
    undo_redo_service.de_redo()
    assert len(rezervare_repository.read()) == 0
    undo_redo_service.do_undo()
    assert len(rezervare_repository.read()) == 4
