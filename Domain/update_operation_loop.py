from typing import List
from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class UpdateOperationLoop(UndoRedoOperation):

    def __init__(self, repository: Repository, entities_before: List[Entity],
                 updated_entities: List[Entity]):
        self.repository = repository
        self.entities_before = entities_before
        self.updated_entities = updated_entities

    def undo(self):
        for entity in self.entities_before:
            self.repository.update(entity)

    def redo(self):
        for updated_entity in self.updated_entities:
            self.repository.update(updated_entity)
