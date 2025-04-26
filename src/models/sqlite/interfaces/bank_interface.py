from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import REAL
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable

class BankInterface(ABC):

    @abstractmethod
    def list_pessoa_fisica(self) -> List[PessoaFisicaTable]:
        pass

    @abstractmethod
    def insert_pessoa_fisica(self,renda_mensal: REAL, idade: int, nome_completo: str, celular: str, email: str, categoria: str, saldo: REAL) -> None:
        pass

    @abstractmethod
    def get_person_fisica(self, person_id: int) -> PessoaFisicaTable:
        pass

    @abstractmethod
    def list_pessoa_juridica(self) -> List[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def insert_pessoa_juridica(self,faturamento: REAL, idade: int, nome_fantasia: str, celular: str, email_corporativo: str, categoria: str, saldo: REAL) -> None:
        pass

    @abstractmethod
    def get_person_juridica(self, person_id: int) -> PessoaJuridicaTable:
        pass
