from typing import List

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class FilmService:
    def __init__(self, film_repository: Repository,
                 film_validator: FilmValidator,
                 undo_redo_service: UndoRedoService):
        self.film_repository = film_repository
        self.film_validator = film_validator
        self.undo_redo_service = undo_redo_service

    def add_film(self, id_film: str, titlu: str, an_aparitie: int,
                 pret_bilet: float, in_program: bool) -> None:
        """
        Adaugarea unui film
        :param id_film: str
        :param titlu: str
        :param an_aparitie: int
        :param pret_bilet: float
        :param in_program: str
        :return:
        """
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.film_validator.validate(film)
        self.film_repository.create(film)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.film_repository, film)
        self.undo_redo_service.add_to_undo(add_operation)

    def get_all_film(self) -> List[Film]:
        """
        preia toate entitatiile
        :return:
        """
        return self.film_repository.read()

    def update_film(self, id_film: str, titlu_new: str, an_aparitie_new: int,
                    pret_bilet_new: float, in_program_new: bool) -> None:
        """
        Modificarea unui film
        :param id_film: str
        :param titlu_new: str
        :param an_aparitie_new: int
        :param pret_bilet_new: float
        :param in_program_new: str
        :return:
        """
        film_inainte = self.film_repository.read(id_film)
        film = Film(id_film, titlu_new, an_aparitie_new,
                    pret_bilet_new, in_program_new)
        self.film_validator.validate(film)
        self.film_repository.update(film)

        self.undo_redo_service.clear_redo()
        updated_operation = UpdateOperation(self.film_repository, film,
                                            film_inainte)
        self.undo_redo_service.add_to_undo(updated_operation)

    def delete_film(self, id_film: str) -> None:
        """
        Stergerea unui film
        :param id_film: str
        :return:
        """
        self.film_repository.delete(id_film)

        self.undo_redo_service.clear_redo()
        delete_oper = DeleteOperation(self.film_repository,
                                      self.film_repository.read(id_film))
        self.undo_redo_service.add_to_undo(delete_oper)
