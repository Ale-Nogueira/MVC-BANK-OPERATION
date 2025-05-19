from unittest import mock
import pytest
from sqlalchemy.orm.exc import NoResultFound
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.entities.extrato import ExtratoTable
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

def test_sacar_dinheiro_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=1800)

    pessoa = mock_connection.session.query(PessoaFisicaTable).filter().one_or_none()

    assert result == "Saque de 1800 realizado com sucesso! Saldo atual: 1200"
    assert pessoa.saldo == 1200
    mock_connection.session.commit.assert_called_once()

def test_saldo_insuficiente_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=4000)

    pessoa = mock_connection.session.query(PessoaFisicaTable).filter().one_or_none()

    assert result == "Saldo insuficiente!"
    assert pessoa.saldo == 3000
    mock_connection.session.commit.assert_not_called()

def test_valor_acima_limite_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=2500)

    pessoa = mock_connection.session.query(PessoaFisicaTable).filter().one_or_none()

    assert result == "O saque não pode exceder 2000 para pessoa física."
    assert pessoa.saldo == 3000
    mock_connection.session.commit.assert_not_called()

def test_adicionar_extrato_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    repo.sacar_dinheiro(person_id=1, valor=1000)

    extrato_adicionado = mock_connection.session.add.call_args[0][0]
    assert isinstance(extrato_adicionado, ExtratoTable)
    assert extrato_adicionado.pessoa_fisica_id == 1
    assert extrato_adicionado.valor == 1000


def test_cliente_nao_encontrado_pessoa_fisica():
    mock_connection = MockConnectionNotFound()
    repo = PessoaFisicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=999, valor=100)

    assert result == "Cliente não encontrado"
    mock_connection.session.commit.assert_not_called()

def test_exception_sacar_dinheiro():
    mock_connection = MockConnectionNoResult()
    repo = PessoaFisicaRepository(mock_connection)

    with pytest.raises(Exception, match="Erro ao realizar saque"):
        repo.sacar_dinheiro(person_id=2, valor= 1800)

    mock_connection.session.rollback.assert_called_once()

def test_realizar_extrato_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    repo.sacar_dinheiro(person_id=2, valor=400)

    response = repo.realizar_extrato(person_id=2)
    mock_connection.session.query.assert_any_call(PessoaFisicaTable)
    mock_connection.session.query.assert_any_call(ExtratoTable)
    assert response["saldo_atual"] == 2600.0
    assert response["saques"] == [{"valor": 400.0}]

def test_extrato_pessoa_fisica_not_found():
    mock_connection = MockConnectionNotFound()
    repo = PessoaFisicaRepository(mock_connection)

    response = repo.realizar_extrato(person_id=99)
    assert response == "Cliente não encontrado"

def test_not_extrato_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    response = repo.realizar_extrato(person_id=2)
    assert response == "Sem movimentação para o cliente 2."

def test_exception_extrato():
    mock_connection = MockConnectionNoResult()
    repo = PessoaFisicaRepository(mock_connection)

    with pytest.raises(Exception, match="Erro ao consultar o extrato"):
        repo.realizar_extrato(person_id=2)

    mock_connection.session.rollback.assert_called_once()
