import pytest
from src.models.sqlite.setting.connection import db_connection_handler
from .pessoa_fisica_repository import PessoaFisicaRepository
from.pessoa_juridica_repository import PessoaJuridicaRepository

#db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="interacao com o banco")
def test_list_pessoas_fisica():
    repo = PessoaFisicaRepository(db_connection_handler)
    response = repo.list_pessoa_fisica()
    print()
    print(response)

@pytest.mark.skip(reason="interacao com o banco")
def test_list_pessoas_juridica():
    repo = PessoaJuridicaRepository(db_connection_handler)
    response = repo.list_pessoa_juridica()
    print()
    print(response)
