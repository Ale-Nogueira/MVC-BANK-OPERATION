from src.models.sqlite.setting.connection import db_connection_handler
from src.models.sqlite.repositories.bank_repository import BankRepository
from src.controllers.bank_controller_pessoa_juridica import BankFinderController, BankListController, BankInsertController
from src.views.bank_view_pessoa_juridica import BankViewListPessoaJuridica, BankViewInsertPessoaJuridica,BankViewFindPessoaJuridica



def list_pessoa_juridica_composer():
    model = BankRepository(db_connection_handler)
    controller = BankListController(model)
    view = BankViewListPessoaJuridica(controller)

    return view

def insert_pessoa_juridica_composer():
    model = BankRepository(db_connection_handler)
    controller = BankInsertController(model)
    view = BankViewInsertPessoaJuridica(controller)

    return view

def find_pessoa_juridica_composer():
    model = BankRepository(db_connection_handler)
    controller = BankFinderController(model)
    view = BankViewFindPessoaJuridica(controller)

    return view
