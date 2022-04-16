from datetime import date, time
from typing import List
import method as method
from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.delete_operation_loop import DeleteOperationLoop
from Domain.film import Film
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.rezervari_in_interval import RezervariInInterval


class RezervareService:
    def __init__(self, rezervare_repository: Repository,
                 rezervare_validator: RezervareValidator,
                 film_repository: Repository,
                 card_client_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.card_client_repository = card_client_repository
        self.film_repository = film_repository
        self.rezervare_repository = rezervare_repository
        self.rezervare_validator = rezervare_validator
        self.undo_redo_service = undo_redo_service

    def add_rezervare(self, id_rezervare: str, id_film: str,
                      id_card_client: str, data: date, ora: time) -> None:
        """
        adauga o rezervare
        :param id_rezervare:
        :param id_film:
        :param id_card_client:
        :param data:
        :param ora:
        :return:
        """

        rez = Rezervare(id_rezervare, id_film, id_card_client, data, ora)
        card_client = self.card_client_repository.read(id_card_client)
        card_client.puncte_acumulate = self.add_points(id_film, id_card_client)
        self.card_client_repository.update(card_client)
        self.rezervare_validator.program_film(id_film)
        self.rezervare_validator.validate(rez, id_film, id_card_client)
        self.rezervare_repository.create(rez)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.rezervare_repository, rez)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_rezervare(self, id_rezervare: str, id_film: str,
                         id_card_client: str, data: date, ora: time) -> None:
        """
        Modificarea rezervarii
        :param id_rezervare:
        :param id_film:
        :param id_card_client:
        :param data:
        :param ora:
        :return:
        """
        rez_inainte = self.rezervare_repository.read(id_rezervare)
        rezervare = Rezervare(id_rezervare, id_film, id_card_client, data, ora)
        self.rezervare_validator.validate(rezervare, id_film, id_card_client)
        self.rezervare_repository.update(rezervare)

        self.undo_redo_service.clear_redo()
        updated_operation = UpdateOperation(self.rezervare_repository,
                                            rezervare, rez_inainte)
        self.undo_redo_service.add_to_undo(updated_operation)

    def get_all_rezervare(self) -> List[Rezervare]:
        """
        returneaaza toate cardurile
        :return:
        """
        return self.rezervare_repository.read()

    def delete_rezervare(self, id_rezervare: str) -> None:
        """
        Stergerea filmului
        :param id_rezervare: str
        :return:
        """
        self.rezervare_repository.delete(id_rezervare)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.rezervare_repository,
                                           self.rezervare_repository.read(
                                               id_rezervare))
        self.undo_redo_service.add_to_undo(delete_operation)

    def add_points(self, id_film: str, id_card_client: str) -> int:
        """
        Clientul acumulează pe card 10% (parte întreagă) din prețul filmului.
        :param id_film:
        :param id_card_client:
        :return:
        """
        film = self.film_repository.read(id_film)
        card = self.card_client_repository.read(id_card_client)
        puncte_bonus = card.puncte_acumulate + int(0.1 * film.pret_bilet)
        return puncte_bonus

    def search_rezervare(self, string: str):
        """
        cautare full text in rezervari
        :param string:
        :return:
        """
        rezultat = []
        rezervari = self.get_all_rezervare()
        for rezervare in rezervari:
            search_rezervrare = str(rezervare.id_entity) + \
                                str(rezervare.id_film) \
                                + str(rezervare.id_card_client) + \
                                rezervare.data.strftime("%d.%m.%Y") + \
                                rezervare.ora.strftime("%H.%M")
            if search_rezervrare.find(string) != -1:
                rezultat.append(rezervare)
        return rezultat

    def search_movie(self, string: str):
        """
        Cautare full text in filme
        :param string: string-ul cautat
        :return: o lista cu enititatiile care contin parametrul string
        """
        rezultat = []
        filme = self.film_repository.read()
        for film in filme:
            search_film = str(film.id_entity) + str(film.titlu) + \
                          str(film.an_aparitie) + \
                          str(film.pret_bilet) + str(film.in_program)
            if search_film.find(string) != -1:
                rezultat.append(film)

        for rez in self.search_rezervare(string):
            rezultat.append(rez)

        if not rezultat:
            rezultat.append("Not found!")
        return rezultat

    def search_card(self, string: str):
        """
        cautare full text in clienti
        :param string: string-ul cautat
        :return: o lista cu enititatiile care contin parametrul string
        """
        rezultat = []
        card_clienti = self.card_client_repository.read()

        for card_client in card_clienti:
            search_card_clienti = str(card_client.id_entity) + \
                                  str(card_client.nume) + \
                                  str(card_client.prenume) + \
                                  str(card_client.CNP) + \
                                  card_client.data_nasterii.strftime(
                                      "%d.%m.%Y") + \
                                  card_client.data_inregistrarii.strftime(
                                      "%d.%m.%Y") + \
                                  str(card_client.puncte_acumulate)
            if search_card_clienti.find(string) != -1:
                rezultat.append(card_client)

        for rez in self.search_rezervare(string):
            rezultat.append(rez)

        if not rezultat:
            rezultat.append("Not found!")
        return rezultat

    def rezervari_interval_ore(self, ora_start: time, ora_stop: time) -> \
            List[RezervariInInterval]:
        """
        Afiș tuturor rezervărilor dintr-un interval de ore dat,
         indiferent de zi.
        :param ora_start:
        :param ora_stop:
        :return:
        """
        rez = self.get_all_rezervare()
        rez_de_determinat = map(lambda rez:
                                RezervariInInterval(rez.id_entity,
                                                    rez.id_film,
                                                    rez.id_card_client,
                                                    rez.ora), rez)

        result = [rezervare for rezervare in rez_de_determinat
                  if ora_start <= rezervare.ora_rezervare <= ora_stop]
        return result

    def nr_rezervari(self, film: Film) -> int:
        """
        Numarul rezervarilor
        :param film:
        :return: numarul de rezervari ale unui film
        """
        rez = self.get_all_rezervare()
        nr = 0
        for i in range(len(rez)):
            if film.id_entity == rez[i].id_film:
                nr += 1
        return nr

    def nr_rez_recursiv(self, film: Film, rez, i) -> int:
        """
        Numarul rezervarilor recursiv
        :param film:
        :param rez:
        :param i:
        :return: numarul de rezervari ale unui film
        """
        if i == len(rez):
            return 0
        if film.id_entity == rez[i].id_film:
            return 1 + self.nr_rez_recursiv(film, rez, i + 1)
        return self.nr_rez_recursiv(film, rez, i + 1)

    @staticmethod
    def sort_method(vector: list, function: method):
        """
        metoda de sortare
        :param vector: sir
        :param function: method (criteriu de sortare)
        :return:
        """
        for i in range(len(vector) - 1):
            for j in range(i + 1, len(vector)):
                if function(vector[i]) < function(vector[j]):
                    vector[i], vector[j] = vector[j], vector[i]
        return vector

    def ordoneaza_filme_dupa_nr_rez(self) -> List[Film]:
        """
        Ordoneaza filme dupa numarul de rezervari
        :return: filmele ordonate dupa nr de rezervari
        """
        filme = self.film_repository.read()
        return self.sort_method(filme, self.nr_rezervari)

    def stergere_rezervari_interval_zile(self,
                                         day_start: date,
                                         day_stop: date) -> None:
        """
        stergerea tuturor rezervarilor dintr-ul interval de zile
        :param day_start:
        :param day_stop:
        :return:
        """
        rez = self.get_all_rezervare()
        if day_stop < day_start:
            raise ValueError("Date introduse gresit!")

        rezervari_de_sters = [rezervare for rezervare in rez
                              if day_start <= rezervare.data <= day_stop]
        for rezervare in rezervari_de_sters:
            self.rezervare_repository.delete(rezervare.id_entity)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperationLoop(self.rezervare_repository,
                                               rezervari_de_sters)
        self.undo_redo_service.add_to_undo(delete_operation)

    def stergere_in_cascada_film(self, id_film_sters: str):
        """
        Stergere in cascada
        :param id_film_sters:
        :return: sterge toate rezervarile cu id-ul id_film_sters
        """
        rez = self.get_all_rezervare()
        result_list = [rezervare for rezervare in rez
                       if rezervare.id_film == id_film_sters]
        for rezervare in result_list:
            self.rezervare_repository.delete(rezervare.id_entity)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperationLoop(self.rezervare_repository,
                                               result_list)

        self.undo_redo_service.add_to_undo(delete_operation)

    def stergere_in_cascada_card_client(self, id_card_sters: str):
        """
        stergere in cascada
        :param id_card_sters:
        :return: sterge toate rezervarile cu id-ul id_card_sters
        """
        rez = self.get_all_rezervare()
        result_list = [rezervare for rezervare in rez
                       if rezervare.id_card_client == id_card_sters]
        for rezervare in result_list:
            self.rezervare_repository.delete(rezervare.id_entity)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperationLoop(self.rezervare_repository,
                                               result_list)
        self.undo_redo_service.add_to_undo(delete_operation)
