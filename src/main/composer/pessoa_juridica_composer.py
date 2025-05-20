from src.models.sqlite.setting.connection import db_connection_handler
from src.models.sqlite.repositories.pessoa_juridica_repository import PessoaJuridicaRepository
from src.controllers.pessoa_juridica_controller import PessoaJuridicaSaqueController, PessoaJuridicaExtratoController
from src.views.pessoa_juridica_view import PessoaJuridicaSaqueView, PessoaJuridicaExtratoView

def saque_pessoa_juridica_composer():
    model = PessoaJuridicaRepository(db_connection_handler)
    controller = PessoaJuridicaSaqueController(model)
    view = PessoaJuridicaSaqueView(controller)

    return view

def extrato_pessoa_juridica_composer():
    model = PessoaJuridicaRepository(db_connection_handler)
    controller = PessoaJuridicaExtratoController(model)
    view = PessoaJuridicaExtratoView(controller)

    return view
