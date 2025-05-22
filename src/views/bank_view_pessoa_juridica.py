from src.controllers.interfaces.bank_controller_pessoa_juridica import BankInsertControllerInterface, BankListControllerInterface, BankFinderControllerInterface
from src.validators.bank_validator import insert_pessoa_juridica_validator
from .http_types.http_request import HttpRequest
from .http_types.https_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class BankViewInsertPessoaJuridica(ViewInterface):
    def __init__(self, controller:BankInsertControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        insert_pessoa_juridica_validator(http_request)

        person_info = http_request.body
        body_response = self.__controller.insert(person_info)

        return HttpResponse(status_code=201, body=body_response)

class BankViewFindPessoaJuridica(ViewInterface):
    def __init__(self, controller:BankFinderControllerInterface) -> None:
        self.__controller = controller


    def handle(self, http_request: HttpRequest) -> HttpResponse:
        person_id = http_request.param["person_id"]
        body_response = self.__controller.find(person_id)

        return HttpResponse(status_code=200, body=body_response)

class BankViewListPessoaJuridica(ViewInterface):
    def __init__(self, controller:BankListControllerInterface) -> None:
        self.__controller = controller


    def handle(self, http_request: HttpRequest) -> HttpResponse:
        body_response = self.__controller.list_pessoa_juridica()

        return HttpResponse(status_code=200, body=body_response)
