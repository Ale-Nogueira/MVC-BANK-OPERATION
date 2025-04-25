import pytest
from .pessoa_fisica_controller import PessoaFisicaSaqueController, PessoaFisicaExtratoController


class MockPessoaFisica:
    def sacar_dinheiro(self, person_id: int, valor: int):
        pass

    def realizar_extrato(self, person_id: int):
        pass

def test_saque():
    saque_info = {
        "person_id": 1,
        "valor": 1000
    }

    controller = PessoaFisicaSaqueController(MockPessoaFisica())
    response = controller.sacar(saque_info)

    assert response["data"]["type"] == "Saque"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == saque_info

def test_saque_error():
    saque_info = {
        "person_id": None,
        "valor": 1000
    }

    controller = PessoaFisicaSaqueController(MockPessoaFisica())

    with pytest.raises(Exception):
        controller.sacar(saque_info)

def test_extrato():
    extrato_info = {
        "person_id": 1
    }

    controller = PessoaFisicaExtratoController(MockPessoaFisica())
    response = controller.extrato(extrato_info)

    assert response["data"]["type"] == "Extrato"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == extrato_info

def test_extrato_error():
    extrato_info = {
        "person_id": None
    }

    controller = PessoaFisicaExtratoController(MockPessoaFisica())

    with pytest.raises(Exception):
        controller.extrato(extrato_info)
