from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class UpdateOperation(UndoRedoOperation):

    def __init__(self, repository: Repository,
                 updated_entity: Entity, entity: Entity):
        self.repository = repository
        self.updated_entity = updated_entity
        self.entity = entity

    def undo(self):
        self.repository.update(self.entity)

    def redo(self):
        self.repository.update(self.updated_entity)
