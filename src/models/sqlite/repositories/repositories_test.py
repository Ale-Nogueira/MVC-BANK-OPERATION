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

@pytest.mark.skip(reason="interacao com o banco")
def test_insert_pessoa_fisica():
    renda_mensal = 5000
    idade = 26
    nome_completo = "fulano de tal"
    celular = "119988554"
    email = "email@test"
    categoria = "categoria A"
    saldo = 10000

    repo = PessoaFisicaRepository(db_connection_handler)
    repo.insert_pessoa_fisica(renda_mensal, idade, nome_completo, celular, email, categoria, saldo)

@pytest.mark.skip(reason="interacao com o banco")
def test_get_pessoa_fisica():
    person_id = 1

    repo = PessoaFisicaRepository(db_connection_handler)
    response = repo.get_person(person_id)
    print()
    print(response)

@pytest.mark.skip(reason="interacao com o banco")
def test_insert_pessoa_juridica():
    faturamento = 100000
    idade = 5
    nome_fantasia = "empresa x"
    celular = "119988554"
    email_corporativo = "email@test"
    categoria = "categoria A"
    saldo = 120000

    repo = PessoaJuridicaRepository(db_connection_handler)
    repo.insert_pessoa_juridica(faturamento, idade, nome_fantasia, celular, email_corporativo, categoria, saldo)

@pytest.mark.skip(reason="interacao com o banco")
def test_get_pessoa_juridica():
    person_id = 1

    repo = PessoaJuridicaRepository(db_connection_handler)
    response = repo.get_person(person_id)
    print()
    print(response)

@pytest.mark.skip(reason="interacao com o banco")
def test_sacar_dinheiro_pessoa_fisica():
    person_id = 1
    valor = 1900

    repo = PessoaFisicaRepository(db_connection_handler)
    response = repo.sacar_dinheiro(person_id, valor)
    print()
    print(response)

@pytest.mark.skip(reason="interacao com o banco")
def test_extrato_pessoa_fisica():
    person_id = 1

    repo = PessoaFisicaRepository(db_connection_handler)
    response = repo.realizar_extrato(person_id)
    print()
    print(response)
