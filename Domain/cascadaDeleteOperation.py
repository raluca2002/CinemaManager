from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class CascadaDeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 rezervareRepository: Repository,
                 cascadeList: List):
        self.__repository = repository
        self.__rezervareRepository = rezervareRepository
        self.__cascadeList = cascadeList

    def doUndo(self):
        for i in range(len(self.__cascadeList) - 1):
            self.__rezervareRepository.read(self.__cascadeList[i])
        self.__repository.read(
            self.__cascadeList[len(self.__cascadeList) - 1]
        )

    def doRedo(self):
        for i in range(len(self.__cascadeList) - 1):
            self.__rezervareRepository.delete(
                self.__cascadeList[0].idEntitate
            )
        self.__repository.delete(
            self.__cascadeList[len(self.__cascadeList) - 1].idEntitate
        )
