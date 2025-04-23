from unittest import mock
import pytest
from sqlalchemy.orm.exc import NoResultFound
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from .pessoa_fisica_repository import PessoaFisicaRepository


class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PessoaFisicaTable)], #query
                    [
                        PessoaFisicaTable(id=2,  nome_completo="fulano", renda_mensal=5000, saldo=3000)
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

class MockConnectionNotFound:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.return_value.filter.return_value.one_or_none.return_value = None

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

def test_list_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)
    response = repo.list_pessoa_fisica()

    mock_connection.session.query.assert_called_once_with(PessoaFisicaTable)
    mock_connection.session.all.assert_called_once()
    mock_connection.session.filter.assert_not_called()

    assert response[0].nome_completo== "fulano"

def test_list_pessoa_fisica_no_result():
    mock_connection = MockConnectionNoResult()
    repo = PessoaFisicaRepository(mock_connection)
    response = repo.list_pessoa_fisica()

    mock_connection.session.query.assert_called_once_with(PessoaFisicaTable)
    mock_connection.session.all.assert_not_called()
    mock_connection.session.filter.assert_not_called()

    assert response == []

def test_insert_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    repo.insert_pessoa_fisica(
        renda_mensal=5000,
        idade=30,
        nome_completo="Fulano de Tal",
        celular="999999999",
        email="Fulano@email.com",
        categoria="Categoria A",
        saldo=1500
    )

    mock_connection.session.add.assert_called_once()
    added_instance = mock_connection.session.add.call_args[0][0]
    assert isinstance(added_instance, PessoaFisicaTable)
    assert added_instance.nome_completo == "Fulano de Tal"

    mock_connection.session.commit.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

def test_insert_pessoa_fisica_exception():
    mock_connection = MockConnectionNoResult()
    repo = PessoaFisicaRepository(mock_connection)

    with pytest.raises(Exception, match="Erro no banco"):
        repo.insert_pessoa_fisica(
            renda_mensal=5000,
            idade=30,
            nome_completo="Maria da Silva",
            celular="888888888",
            email="maria@email.com",
            categoria="vip",
            saldo=2000
        )

    mock_connection.session.rollback.assert_called_once()

def test_sacar_dinheiro_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=1800)

    pessoa = mock_connection.session.query(PessoaFisicaTable).filter().one_or_none()

    assert result == "Saque de 1800 realizado com sucesso! Saldo atual: 1200"
    assert pessoa.saldo == 1200
    mock_connection.session.commit.assert_called_once()

def test_sacar_dinheiro_saldo_insuficiente():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=4000)

    pessoa = mock_connection.session.query(PessoaFisicaTable).filter().one_or_none()

    assert result == "Saldo insuficiente!"
    assert pessoa.saldo == 3000
    mock_connection.session.commit.assert_not_called()

def test_sacar_dinheiro_valor_acima_limite():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=2500)

    pessoa = mock_connection.session.query(PessoaFisicaTable).filter().one_or_none()

    assert result == "O saque não pode exceder 2000 para pessoa física."
    assert pessoa.saldo == 3000  # saldo original
    mock_connection.session.commit.assert_not_called()

def test_sacar_dinheiro_cliente_nao_encontrado():
    mock_connection = MockConnectionNotFound()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=999, valor=100)

    assert result == "Cliente não encontrado"
    mock_connection.session.commit.assert_not_called()
