# pylint: disable=W0613:unused-argument
import pytest
from .pessoa_juridica_controller import PessoaJuridicaSaqueController, PessoaJuridicaExtratoController


class MockPessoaJuridica:
    def sacar_dinheiro(self, person_id: int, valor: int):
        pass

    def realizar_extrato(self, person_id: int):
        return {
            "saques": [{"valor": 1000.0}],
            "saldo_atual": 9000.0
        }

def test_saque():
    saque_info = {
        "person_id": 1,
        "valor": 1000
    }

    controller = PessoaJuridicaSaqueController(MockPessoaJuridica())
    response = controller.sacar(saque_info)

    assert response["data"]["type"] == "Saque"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == saque_info

def test_saque_error():
    saque_info = {
        "person_id": None,
        "valor": 1000
    }

    controller = PessoaJuridicaSaqueController(MockPessoaJuridica())

    with pytest.raises(Exception):
        controller.sacar(saque_info)

def test_extrato():
    extrato_info = {
        "person_id": 1
    }

    controller = PessoaJuridicaExtratoController(MockPessoaJuridica())
    response = controller.extrato(extrato_info)

    assert response["data"]["type"] == "Extrato"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"]["saques"] == [{"valor": 1000.0}]
    assert response["data"]["attributes"]["saldo_atual"] == 9000.0

def test_extrato_error():
    extrato_info = {
        "person_id": None
    }

    controller = PessoaJuridicaExtratoController(MockPessoaJuridica())

    with pytest.raises(Exception):
        controller.extrato(extrato_info)
