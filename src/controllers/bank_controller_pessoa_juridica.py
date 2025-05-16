from typing import List
import re
from src.models.sqlite.interfaces.bank_interface import BankInterface
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from .interfaces.bank_controller_pessoa_juridica import BankFinderControllerInterface, BankInsertControllerInterface, BankListControllerInterface

class BankListController(BankListControllerInterface):
    def __init__(self, bank_repository: BankInterface) -> None:
        self.__bank_repository = bank_repository

    def list_pessoa_juridica(self) -> dict:
        pessoa_juridica = self.__get_person_in_db()
        response = self.__format_response(pessoa_juridica)
        return response

    def __get_person_in_db(self) -> List[PessoaJuridicaTable]:
        pessoa_juridica = self.__bank_repository.list_pessoa_juridica()
        return pessoa_juridica

    def __format_response(self, pessoa_juridica: List[PessoaJuridicaTable]) -> dict:
        formatted_pessoa_juridica = []
        for pessoa in pessoa_juridica:
            formatted_pessoa_juridica.append({"nome_fantasia": pessoa.nome_fantasia, "email_corporativo": pessoa.email_corporativo, "faturamento":pessoa.faturamento})

        return {
            "data": {
                "type": "Pessoa Juridica",
                "count": len(formatted_pessoa_juridica),
                "attributes": formatted_pessoa_juridica
            }
        }

class BankInsertController(BankInsertControllerInterface):
    def __init__(self, bank_repository: BankInterface) -> None:
        self.__bank_repository = bank_repository

    def insert(self, person_info: dict) -> dict:
        faturamento=person_info["faturamento"]
        idade=person_info["idade"]
        nome_fantasia=person_info["nome_fantasia"]
        celular=person_info["celular"]
        email_corporativo=person_info["email_corporativo"]
        categoria=person_info["categoria"]
        saldo=person_info["saldo"]

        self.__validade_nome_fantasia(nome_fantasia)
        self.__insert_person_in_db(faturamento, idade, nome_fantasia, celular, email_corporativo, categoria, saldo)
        formated_response = self.__format_response(person_info)
        return formated_response

    def __validade_nome_fantasia(self, nome_fantasia: str) -> None:
        non_valid_caracteres = re.compile(r'[^a-zA-Z\s]')

        if non_valid_caracteres.search(nome_fantasia):
            raise Exception("Nome da empresa invalido!")

    def __insert_person_in_db(self, faturamento= int, idade=int, nome_fantasia= str, celular= int, email_corporativo= str, categoria= str, saldo= int) -> None:
        self.__bank_repository.insert_pessoa_juridica(faturamento, idade, nome_fantasia, celular, email_corporativo, categoria, saldo)

    def __format_response(self, person_info: dict) -> dict:
        return {
            "data": {
                "type": "Pessoa Juridica",
                "count": 1,
                "attributes": person_info
            }
        }

class BankFinderController(BankFinderControllerInterface):
    def __init__(self, bank_repository: BankInterface) -> None:
        self.__bank_repository = bank_repository

    def find(self, person_id) -> dict:
        person = self.__find_person_ind_db(person_id)
        response = self.__format_response(person)
        return response

    def __find_person_ind_db(self, person_id: int) -> PessoaJuridicaTable:
        person = self.__bank_repository.get_person_juridica(person_id)
        if not person:
            raise Exception("Empresa não encontrada!")

        return person

    def __format_response(self, person: PessoaJuridicaTable) -> dict:
        return {
            "data": {
                "type": "Pessoa Juridica",
                "count": 1,
                "attributes": {
                    "nome_fantasia": person.nome_fantasia,
                    "email_corporativo": person.email_corporativo,
                    "faturamento": person.faturamento
                }
            }
        }
