from abc import ABC, abstractmethod

class BankListControllerInterface(ABC):

    @abstractmethod
    def list_pessoa_juridica(self) -> dict:
        pass

class BankInsertControllerInterface(ABC):

    @abstractmethod
    def insert(self, person_info: dict) -> dict:
        pass

class BankFinderControllerInterface(ABC):

    @abstractmethod
    def find(self, person_id) -> dict:
        pass
