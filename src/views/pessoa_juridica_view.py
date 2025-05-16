from src.controllers.interfaces.pessoa_juridica_controller import PessoaJuridicaSaqueControllerInterface, PessoaJuridicaExtratoControllerInterface
from .http_types.http_request import HttpRequest
from .http_types.https_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class PessoaJuridicaSaqueView(ViewInterface):
    def __init__(self, controller: PessoaJuridicaSaqueControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        saque_info = http_request.body
        body_response = self.__controller.sacar(saque_info)

        return HttpResponse(status_code=200, body=body_response)

class PessoaJuridicaExtratoView(ViewInterface):
    def __init__(self, controller: PessoaJuridicaExtratoControllerInterface) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        extrato_info = http_request.body
        body_response = self.__controller.extrato(extrato_info)

        return HttpResponse(status_code=200, body=body_response)
