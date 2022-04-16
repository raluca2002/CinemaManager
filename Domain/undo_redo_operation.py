from abc import ABC, abstractmethod


class UndoRedoOperation(ABC):

    @abstractmethod
    def undo(self):
        ...

    def redo(self):
        ...
