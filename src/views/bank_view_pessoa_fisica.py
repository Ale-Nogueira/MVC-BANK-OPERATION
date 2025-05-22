from src.controllers.interfaces.bank_controller_pessoa_fisica import BankInsertControllerInterface, BankListControllerInterface, BankFinderControllerInterface
from src.validators.bank_validator import insert_pessoa_fisica_validator
from .http_types.http_request import HttpRequest
from .http_types.https_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class BankViewInsertPessoaFisica(ViewInterface):
    def __init__(self, controller:BankInsertControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        insert_pessoa_fisica_validator(http_request)

        person_info = http_request.body
        body_response = self.__controller.insert(person_info)

        return HttpResponse(status_code=201, body=body_response)

class BankViewFindPessoaFisica(ViewInterface):
    def __init__(self, controller:BankFinderControllerInterface) -> None:
        self.__controller = controller


    def handle(self, http_request: HttpRequest) -> HttpResponse:
        person_id = http_request.param["person_id"]
        body_response = self.__controller.find(person_id)

        return HttpResponse(status_code=200, body=body_response)

class BankViewListPessoaFisica(ViewInterface):
    def __init__(self, controller:BankListControllerInterface) -> None:
        self.__controller = controller


    def handle(self, http_request: HttpRequest) -> HttpResponse:
        body_response = self.__controller.list_pessoa_fisica()

        return HttpResponse(status_code=200, body=body_response)
