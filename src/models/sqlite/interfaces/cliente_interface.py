from abc import ABC, abstractmethod
from sqlalchemy import REAL

class ClienteInterface(ABC):

    @abstractmethod
    def sacar_dinheiro(self, person_id: int, valor: REAL) -> str:
        pass

    @abstractmethod
    def realizar_extrato(self, person_id: int) -> str:
        pass
