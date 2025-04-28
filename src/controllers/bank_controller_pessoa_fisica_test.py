#pylint: disable=unused-argument
import pytest
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from .bank_controller_pessoa_fisica import BankListController
from .bank_controller_pessoa_fisica import BankInsertController
from .bank_controller_pessoa_fisica import BankFinderController

class MockPerson():
    def __init__(self, nome_completo, idade, saldo) -> None:
        self.nome_completo = nome_completo
        self.idade = idade
        self.saldo = saldo

class MockBankRepository:
    def list_pessoa_fisica(self):
        return [
            PessoaFisicaTable(nome_completo="fulano de tal", idade=18, email="fulano@email.com", id=1),
            PessoaFisicaTable(nome_completo="ciclano de tal", idade=21, email="ciclano@email.com", id=2)
        ]

    def insert_pessoa_fisica(self, renda_mensal: int, idade: int, nome_completo: str, celular: str, email: str, categoria: str, saldo: int) -> None:
        pass

    def get_person_fisica(self, person_id: int):
        return MockPerson(
            nome_completo="fulano de tal",
            idade=25,
            saldo=3000
        )

def test_list():
    controller = BankListController(MockBankRepository())
    response = controller.list_pessoa_fisica()

    expected_response = {
        "data": {
            "type": "Pessoa Fisica",
            "count": 2,
            "attributes": [
                {"nome_completo": "fulano de tal", "idade": 18, "email": "fulano@email.com", "id": 1},
                {"nome_completo": "ciclano de tal", "idade": 21, "email": "ciclano@email.com", "id": 2}
            ]
        }
    }

    assert response == expected_response

def test_insert():
    person_info = {
        "renda_mensal": 5000,
        "idade": 25,
        "nome_completo": "fulano de tal",
        "celular": "99885544",
        "email": "fulano@email.com",
        "categoria": "categoria A",
        "saldo": 3000
    }

    controller = BankInsertController(MockBankRepository())
    response =  controller.insert(person_info)

    assert response["data"]["type"] == "Pessoa Fisica"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == person_info

def test_insert_error():
    person_info = {
        "renda_mensal": 5000,
        "idade": 25,
        "nome_completo": "fulano123",
        "celular": "99885544",
        "email": "fulano@email.com",
        "categoria": "categoria A",
        "saldo": 3000
    }

    controller = BankInsertController(MockBankRepository())
    with pytest.raises(Exception):
        controller.insert(person_info)

def test_find():
    controller = BankFinderController(MockBankRepository())
    response = controller.find(123)

    expected_response = {
        "data": {
            "type": "Pessoa Fisica",
            "count": 1,
            "attributes": {
                "nome_completo": "fulano de tal",
                "idade": 25,
                "saldo": 3000
            }
        }
    }

    assert response == expected_response
