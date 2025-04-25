from unittest import mock
import pytest
from sqlalchemy.orm.exc import NoResultFound
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.entities.extrato import ExtratoTable
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

class MockConnectionNotFound:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.return_value.filter.return_value.one_or_none.return_value = None

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

def test_sacar_dinheiro_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=3000)

    pessoa = mock_connection.session.query(PessoaJuridicaTable).filter().one_or_none()

    assert result == "Saque de 3000 realizado com sucesso! Saldo atual: 47000"
    assert pessoa.saldo == 47000
    mock_connection.session.commit.assert_called_once()

def test_saldo_insuficiente_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=60000)

    pessoa = mock_connection.session.query(PessoaJuridicaTable).filter().one_or_none()

    assert result == "Saldo insuficiente!"
    assert pessoa.saldo == 50000
    mock_connection.session.commit.assert_not_called()

def test_valor_acima_limite_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=2, valor=11000)

    pessoa = mock_connection.session.query(PessoaJuridicaTable).filter().one_or_none()

    assert result == "O saque não pode exceder 10000 para pessoa juridica."
    assert pessoa.saldo == 50000
    mock_connection.session.commit.assert_not_called()

def test_adicionar_extrato_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    repo.sacar_dinheiro(person_id=1, valor=1000)

    extrato_adicionado = mock_connection.session.add.call_args[0][0]
    assert isinstance(extrato_adicionado, ExtratoTable)
    assert extrato_adicionado.pessoa_juridica_id == 1
    assert extrato_adicionado.valor == 1000

def test_cliente_nao_encontrado_pessoa_juridica():
    mock_connection = MockConnectionNotFound()
    repo = PessoaJuridicaRepository(mock_connection)

    result = repo.sacar_dinheiro(person_id=999, valor=100)

    assert result == "Empresa não encontrada"
    mock_connection.session.commit.assert_not_called()

def test_exception_sacar_dinheiro():
    mock_connection = MockConnectionNoResult()
    repo = PessoaJuridicaRepository(mock_connection)

    with pytest.raises(Exception, match="Erro ao realizar saque"):
        repo.sacar_dinheiro(person_id=2, valor= 1800)

    mock_connection.session.rollback.assert_called_once()

def test_realizar_extrato_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    repo.sacar_dinheiro(person_id=2, valor=4000)

    response = repo.realizar_extrato(person_id=2)
    mock_connection.session.query.assert_any_call(PessoaJuridicaTable)
    mock_connection.session.query.assert_any_call(ExtratoTable)
    assert "Saque de R$4000.00" in response
    assert "Saldo atual: R$46000.00" in response

def test_extrato_pessoa_juridica_not_found():
    mock_connection = MockConnectionNotFound()
    repo = PessoaJuridicaRepository(mock_connection)

    response = repo.realizar_extrato(person_id=99)
    assert response == "Empresa não encontrada"

def test_not_extrato_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    response = repo.realizar_extrato(person_id=2)
    assert response == "Sem movimentação para a empresa 2."

def test_exception_extrato():
    mock_connection = MockConnectionNoResult()
    repo = PessoaJuridicaRepository(mock_connection)

    with pytest.raises(Exception, match="Erro ao consultar o extrato"):
        repo.realizar_extrato(person_id=2)

    mock_connection.session.rollback.assert_called_once()
