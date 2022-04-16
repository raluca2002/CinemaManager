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


def test_full_text_search():
    filename_card = 'test_card.json'
    filename_film = 'test_film.json'
    filename_rezervare = 'test_rezervare.json'
    clear_file(filename_card)
    clear_file(filename_rezervare)
    card_client_repository = JsonRepository(filename_card)
    card_client_validator = CardClientValidator(card_client_repository)
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    film_repository = JsonRepository(filename_film)
    rezervare_repository = JsonRepository(filename_rezervare)
    rezervare_validator = RezervareValidator(film_repository,
                                             card_client_repository)
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    card_client_service.add_card("1006", "Buga", "Ioana", 2981103064557,
                                 datetime.strptime(
                                     "03.11.1998", '%d.%m.%Y').date(),
                                 datetime.strptime(
                                     "21.12.2021", '%d.%m.%Y').date(), 14)
    assert rezervare_service.search_card("ana") == \
           card_client_service.get_all_card()
    lst_error = ["Not found!"]
    assert rezervare_service.search_card("1979") == lst_error
    assert rezervare_service.search_card("liuhfdsi") == lst_error
