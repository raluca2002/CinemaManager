from Domain.film_validator import FilmValidator
from Repository.json_repository import JsonRepository
from Service.film_service import FilmService
from Service.undo_redo_service import UndoRedoService
from utiles import clear_file


def test_card_client_service_add():
    filename = 'test_film.json'
    clear_file(filename)
    film_repository = JsonRepository(filename)
    film_validator = FilmValidator()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)
    film_service.add_film("1001", "Troy", 1990, 19.90, True)
    assert len(film_service.get_all_film()) == 1
    assert film_service.get_all_film()[0].titlu == "Troy"
    try:
        film_service.add_film("", "Omul", 2019, 100, False)
        assert False
    except Exception as e:
        assert True
        assert str(e) == "['ID-ul nu poate fi vid!']"
    try:
        film_service.add_film("1002", "Omul", -2019, -100, False)
        assert False
    except Exception as ex:
        assert True
        assert str(ex) == "['Pretul biletului trebuie sa " \
                          "fie un numar pozitiv!'," \
                          " 'Anul de aparatie nu poate sa fie " \
                          "un numar negativ!']"
