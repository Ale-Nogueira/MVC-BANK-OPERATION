from typing import List
import re
from src.models.sqlite.interfaces.bank_interface import BankInterface
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class BankListPessoaFisicaController:
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

class BankInsertPessoaFisicaController:
    def __init__(self, bank_repository: BankInterface) -> None:
        self.__bank_repository = bank_repository

    def insert(self, person_info: dict) -> dict:
        renda_mensal=person_info["renda_mensal"]
        idade=person_info["idade"]
        nome_completo=person_info["nome_completo"]
        celular=person_info["celular"]
        email=person_info["email"]
        categoria=person_info["categoria"]
        saldo=person_info["saldo"]

        self.__validade_nome_completo(nome_completo)
        self.__insert_person_in_db(renda_mensal, idade, nome_completo, celular, email, categoria, saldo)
        formated_response = self.__format_response(person_info)
        return formated_response

    def __validade_nome_completo(self, nome_completo: str) -> None:
        non_valid_caracteres = re.compile(r'[^a-zA-Z\s]')

        if non_valid_caracteres.search(nome_completo):
            raise Exception("Nome da pessoa invalido!")

    def __insert_person_in_db(self, renda_mensal= int, idade=int, nome_completo= str, celular= int, email= str, categoria= str, saldo= int) -> None:
        self.__bank_repository.insert_pessoa_fisica(renda_mensal, idade, nome_completo, celular, email, categoria, saldo)

    def __format_response(self, person_info: dict) -> dict:
        return {
            "data": {
                "type": "Pessoa Fisica",
                "count": 1,
                "attributes": person_info
            }
        }
