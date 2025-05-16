from src.controllers.interfaces.bank_controller_pessoa_fisica import BankListControllerInterface
from .http_types.http_request import HttpRequest
from .http_types.https_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class BankViewListPessoaFisica(ViewInterface):
    def __init__(self, controller:BankListControllerInterface) -> None:
        self.controller = controller


    def handle(self, http_resquest: HttpRequest) -> HttpResponse:
        pass
