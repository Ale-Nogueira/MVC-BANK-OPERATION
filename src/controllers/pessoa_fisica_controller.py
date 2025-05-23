from src.models.sqlite.interfaces.cliente_interface import ClienteInterface
from src.errors.error_types.http_bad_request import HttpBadRequestError
from .interfaces.pessoa_fisica_controller import PessoaFisicaExtratoControllerInterface, PessoaFisicaSaqueControllerInterface
class PessoaFisicaSaqueController(PessoaFisicaSaqueControllerInterface):
    def __init__(self, pessoa_fisica_repository: ClienteInterface) -> None:
        self.__pessoa_fisica_repository = pessoa_fisica_repository

    def sacar(self, saque_info: dict) -> dict:
        person_id = saque_info["person_id"]
        valor = saque_info["valor"]

        self.__validate_id_and_valor(person_id, valor)
        self.__sacar_dinheiro(person_id, valor)
        formated_response = self.__format_response(saque_info)
        return formated_response

    def __validate_id_and_valor(self, person_id: int, valor: int) -> None:
        if person_id is None or valor is None:
            raise HttpBadRequestError("ID e valor são obrigatórios.")

    def __sacar_dinheiro(self, person_id: int, valor: int) -> None:
        self.__pessoa_fisica_repository.sacar_dinheiro(person_id,valor)

    def __format_response(self, saque_info: dict) -> dict:
        return {
            "data": {
                "type": "Saque",
                "count": 1,
                "attributes": saque_info
            }
        }

class PessoaFisicaExtratoController(PessoaFisicaExtratoControllerInterface):
    def __init__(self, pessoa_fisica_repository: ClienteInterface) -> None:
        self.__pessoa_fisica_repository = pessoa_fisica_repository

    def extrato(self, extrato_info: dict) -> None:
        person_id = extrato_info["person_id"]

        self.__validate_id(person_id)
        extrato_info = self.__realizar_extrato(person_id)
        formated_response = self.__format_response(extrato_info)
        return formated_response

    def __validate_id(self, person_id: int) -> None:
        if person_id is None:
            raise HttpBadRequestError("ID obrigatório.")

    def __realizar_extrato(self, person_id: int) -> dict:
        return self.__pessoa_fisica_repository.realizar_extrato(person_id)

    def __format_response(self, extrato_info: dict) -> dict:
        return {
            "data": {
                "type": "Extrato",
                "count": len(extrato_info["saques"]),
                "attributes": extrato_info
            }
        }
