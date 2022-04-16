from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class DeleteOperation(UndoRedoOperation):

    def __init__(self, repository: Repository,
                 deleted_entity: Entity):
        self.repository = repository
        self.deleted_entity = deleted_entity

    def undo(self):
        self.repository.create(self.deleted_entity)

    def redo(self):
        self.repository.delete(self.deleted_entity.id_entity)
