from src.models.sqlite.setting.connection import db_connection_handler
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository
from src.controllers.pessoa_fisica_controller import PessoaFisicaSaqueController, PessoaFisicaExtratoController
from src.views.pessoa_fisica_view import PessoaFisicaSaqueView, PessoaFisicaExtratoView

def saque_pessoa_fisica_composer():
    model = PessoaFisicaRepository(db_connection_handler)
    controller = PessoaFisicaSaqueController(model)
    view = PessoaFisicaSaqueView(controller)

    return view

def extrato_pessoa_fisica_composer():
    model = PessoaFisicaRepository(db_connection_handler)
    controller = PessoaFisicaExtratoController(model)
    view = PessoaFisicaExtratoView(controller)

    return view
