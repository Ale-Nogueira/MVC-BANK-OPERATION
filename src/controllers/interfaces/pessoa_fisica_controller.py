from abc import ABC, abstractmethod

class PessoaFisicaSaqueControllerInterface(ABC):

    @abstractmethod
    def sacar(self, saque_info: dict) -> dict:
        pass

class PessoaFisicaExtratoControllerInterface(ABC):

    @abstractmethod
    def extrato(self, extrato_info: dict) -> None:
        pass
