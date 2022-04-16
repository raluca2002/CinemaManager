from Domain.card_client_validator import CardClientValidator
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.test_domain import test_film
from Tests.test_full_text import test_full_text_search
from Tests.test_incrementare_pct_card import \
    test_incrementare_puncte_card_client
from Tests.test_ordonare_card_client import test_ordonare_card_client
from Tests.test_ordonare_film import test_ordonare_film
from Tests.test_repository import test_repository
from Tests.test_service import test_card_client_service_add
from Tests.test_stergere_cascada import test_stergere_in_cascada
from Tests.test_stergere_rezervare_interval import \
    test_stergere_rezervare_interval_data
from Tests.test_undo_redo import test_undo_redo
from UI.console import Console


def main():
    film_repository = JsonRepository("filme.json")
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)
    card_client_repository = JsonRepository("card_client.json")
    card_client_validator = CardClientValidator(card_client_repository)
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    rezervare_repository = JsonRepository("rezervare.json")
    rezervare_validator = RezervareValidator(film_repository,
                                             card_client_repository)
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    console = Console(film_service, card_client_service, rezervare_service,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    test_repository()
    test_ordonare_card_client()
    test_film()
    test_card_client_service_add()
    test_full_text_search()
    test_ordonare_film()
    test_stergere_rezervare_interval_data()
    test_stergere_in_cascada()
    test_incrementare_puncte_card_client()
    test_undo_redo()
    main()
