from Domain.entity import Entity
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, idEntitate=None):
        if idEntitate is None:
            return list(self.entitati.values())

        if str(idEntitate) in self.entitati:
            return self.entitati[str(idEntitate)]
        else:
            return None

    def add(self, entitate: Entity):
        """
        Adauga entitate
        :param entitate: clasa
        :return: adaugarea clasei
        """
        if self.read(entitate.id_entity) is not None:
            raise KeyError("Exista deja o entitate cu id-ul dat!")
        self.entitati[str(entitate.id_entity)] = entitate

    def delete(self, id_entity):
        """
        Stergere entitate
        :param idEntitate: id-ul entitatii
        :return: stergerea id-ului
        """
        if self.read(id_entity) is None:
            raise KeyError("Nu exista o entitate cu id-ul dat!")
        del self.entitati[str(id_entity)]

    def update(self, entitate: Entity):
        """
        Modifica entitate
        :param entitate: modificarea clasei
        :return: modificarea clasei
        """
        if self.read(entitate.id_entity) is None:
            raise KeyError("Nu exista o entitate cu id-ul dat!")
        self.entitati[str(entitate.id_entity)] = entitate
