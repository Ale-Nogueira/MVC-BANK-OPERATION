from unittest import mock
import pytest
from sqlalchemy.orm.exc import NoResultFound
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from .pessoa_juridica_repository import PessoaJuridicaRepository


class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PessoaJuridicaTable)], #query
                    [
                        PessoaJuridicaTable(id=2, nome_fantasia="empresa x", faturamento=120000, saldo=50000)
                    ], #resultado

                )

            ]
        )
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.commit.side_effect = Exception("Erro no banco")
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

def test_list_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)
    response = repo.list_pessoa_juridica()

    mock_connection.session.query.assert_called_once_with(PessoaJuridicaTable)
    mock_connection.session.all.assert_called_once()
    mock_connection.session.filter.assert_not_called()

    assert response[0].nome_fantasia== "empresa x"

def test_list_pessoa_juridica_no_result():
    mock_connection = MockConnectionNoResult()
    repo = PessoaJuridicaRepository(mock_connection)
    response = repo.list_pessoa_juridica()

    mock_connection.session.query.assert_called_once_with(PessoaJuridicaTable)
    mock_connection.session.all.assert_not_called()
    mock_connection.session.filter.assert_not_called()

    assert response == []

def test_insert_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    repo.insert_pessoa_juridica(
        faturamento=50000,
        idade=5,
        nome_fantasia="Empresa x",
        celular="999999999",
        email_corporativo="Empresa@email.com",
        categoria="Categoria A",
        saldo=30000
    )

    mock_connection.session.add.assert_called_once()
    added_instance = mock_connection.session.add.call_args[0][0]
    assert isinstance(added_instance, PessoaJuridicaTable)
    assert added_instance.nome_fantasia == "Empresa x"

    mock_connection.session.commit.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

def test_insert_pessoa_juridica_exception():
    mock_connection = MockConnectionNoResult()
    repo = PessoaJuridicaRepository(mock_connection)

    with pytest.raises(Exception, match="Erro no banco"):
        repo.insert_pessoa_juridica(
            faturamento=50000,
            idade=5,
            nome_fantasia="Empresa Y",
            celular="888888888",
            email_corporativo="EmpresaY@email.com",
            categoria="vip",
            saldo=20000
        )

    mock_connection.session.rollback.assert_called_once()

def test_sacar_dinheiro_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=3000)

    pessoa = mock_connection.session.query(PessoaJuridicaTable).filter().one_or_none()

    assert result == "Saque de 3000 realizado com sucesso! Saldo atual: 47000"
    assert pessoa.saldo == 47000
    mock_connection.session.commit.assert_called_once()
