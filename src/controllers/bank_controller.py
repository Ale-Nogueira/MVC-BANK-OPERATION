from typing import List
from src.models.sqlite.interfaces.bank_interface import BankInterface
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class BankListController:
    def __init__(self, bank_repository: BankInterface) -> None:
        self.__bank_repository = bank_repository

    def list_pessoa_fisica(self) -> dict:
        pessoa_fisica = self.__get_person_in_db()
        response = self.__format_response(pessoa_fisica)
        return response

    def __get_person_in_db(self) -> List[PessoaFisicaTable]:
        pessoa_fisica = self.__bank_repository.list_pessoa_fisica()
        return pessoa_fisica

    def __format_response(self, pessoa_fisica: List[PessoaFisicaTable]) -> dict:
        formatted_pessoa_fisica = []
        for pessoa in pessoa_fisica:
            formatted_pessoa_fisica.append({"nome_completo": pessoa.nome_completo, "idade": pessoa.idade, "email": pessoa.email, "id": pessoa.id})

        return {
            "data": {
                "type": "Pessoa Fisica",
                "count": len(formatted_pessoa_fisica),
                "attributes": formatted_pessoa_fisica
            }
        }
