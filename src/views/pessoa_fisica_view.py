from src.controllers.interfaces.pessoa_fisica_controller import PessoaFisicaSaqueControllerInterface, PessoaFisicaExtratoControllerInterface
from .http_types.http_request import HttpRequest
from .http_types.https_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class PessoaFisicaSaqueView(ViewInterface):
    def __init__(self, controller: PessoaFisicaSaqueControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        saque_info = http_request.body
        body_response = self.__controller.sacar(saque_info)

        return HttpResponse(status_code=200, body=body_response)

class PessoaFisicaExtratoView(ViewInterface):
    def __init__(self, controller: PessoaFisicaExtratoControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        extrato_info = http_request.body
        body_response = self.__controller.extrato(extrato_info)

        return HttpResponse(status_code=200, body=body_response)
