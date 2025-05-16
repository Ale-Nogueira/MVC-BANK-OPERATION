from abc import ABC, abstractmethod

class PessoaJuridicaSaqueControllerInterface(ABC):

    @abstractmethod
    def sacar(self, saque_info: dict) -> dict:
        pass

class PessoaJuridicaExtratoControllerInterface(ABC):

    @abstractmethod
    def extrato(self, extrato_info: dict) -> None:
        pass
