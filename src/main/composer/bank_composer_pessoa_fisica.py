from src.models.sqlite.setting.connection import db_connection_handler
from src.models.sqlite.repositories.bank_repository import BankRepository
from src.controllers.bank_controller_pessoa_fisica import BankFinderController, BankListController, BankInsertController
from src.views.bank_view_pessoa_fisica import BankViewListPessoaFisica, BankViewInsertPessoaFisica, BankViewFindPessoaFisica



def list_pessoa_fisica_composer():
    model = BankRepository(db_connection_handler)
    controller = BankListController(model)
    view = BankViewListPessoaFisica(controller)

    return view

def insert_pessoa_fisica_composer():
    model = BankRepository(db_connection_handler)
    controller = BankInsertController(model)
    view = BankViewInsertPessoaFisica(controller)

    return view

def find_pessoa_fisica_composer():
    model = BankRepository(db_connection_handler)
    controller = BankFinderController(model)
    view = BankViewFindPessoaFisica(controller)

    return view
