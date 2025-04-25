import pytest
from .pessoa_fisica_controller import PessoaFisicaSaqueController

class MockSaquePessoaFisica:
    def sacar_dinheiro(self, person_id: int, valor: int):
        pass

def test_saque_pessoa_fisica():
    saque_info = {
        "person_id": 1,
        "valor": 1000
    }

    controller = PessoaFisicaSaqueController(MockSaquePessoaFisica())
    response = controller.sacar(saque_info)

    assert response["data"]["type"] == "Saque"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == saque_info

def test_saque_pessoa_fisica_error():
    saque_info = {
        "person_id": None,
        "valor": 1000
    }

    controller = PessoaFisicaSaqueController(MockSaquePessoaFisica())

    with pytest.raises(Exception):
        controller.sacar(saque_info)
