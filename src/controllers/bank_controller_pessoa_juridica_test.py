#pylint: disable=unused-argument
import pytest
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from .bank_controller_pessoa_juridica import BankListController
from .bank_controller_pessoa_juridica import BankInsertController
from .bank_controller_pessoa_juridica import BankFinderController

class MockPerson():
    def __init__(self, nome_fantasia, email_corporativo, faturamento) -> None:
        self.nome_fantasia = nome_fantasia
        self.email_corporativo = email_corporativo
        self.faturamento = faturamento

class MockBankRepository:
    def list_pessoa_juridica(self):
        return [
            PessoaJuridicaTable(nome_fantasia="Empresa x", faturamento=100000, email_corporativo="empresax@email.com", id=1),
            PessoaJuridicaTable(nome_fantasia="Empresa y", faturamento=150000, email_corporativo="empresay@email.com", id=2)
        ]

    def insert_pessoa_juridica(self, faturamento: int, idade: int, nome_fantasia: str, celular: str, email_corporativo: str, categoria: str, saldo: int) -> None:
        pass

    def get_person_juridica(self, person_id: int):
        return MockPerson(
            nome_fantasia="Empresa x",
            email_corporativo="empresax@email.com",
            faturamento=100000
        )

def test_list():
    controller = BankListController(MockBankRepository())
    response = controller.list_pessoa_juridica()

    expected_response = {
        "data": {
            "type": "Pessoa Juridica",
            "count": 2,
            "attributes": [
                {"nome_fantasia": "Empresa x", "faturamento": 100000, "email_corporativo": "empresax@email.com"},
                {"nome_fantasia": "Empresa y", "faturamento": 150000, "email_corporativo": "empresay@email.com"}
            ]
        }
    }

    assert response == expected_response

def test_insert():
    person_info = {
        "faturamento": 100000,
        "idade": 10,
        "nome_fantasia": "Empresa x",
        "celular": "99885544",
        "email_corporativo": "Empresax@email.com",
        "categoria": "categoria A",
        "saldo": 50000
    }

    controller = BankInsertController(MockBankRepository())
    response =  controller.insert(person_info)

    assert response["data"]["type"] == "Pessoa Juridica"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == person_info

def test_insert_error():
    person_info = {
        "faturamento": 100000,
        "idade": 10,
        "nome_fantasia": "fulano123",
        "celular": "99885544",
        "email_corporativo": "empresax@email.com",
        "categoria": "categoria A",
        "saldo": 50000
    }

    controller = BankInsertController(MockBankRepository())
    with pytest.raises(Exception):
        controller.insert(person_info)

def test_find():
    controller = BankFinderController(MockBankRepository())
    response = controller.find(123)

    expected_response = {
        "data": {
            "type": "Pessoa Juridica",
            "count": 1,
            "attributes": {
                "nome_fantasia": "Empresa x",
                "email_corporativo": "empresax@email.com",
                "faturamento": 100000
            }
        }
    }

    assert response == expected_response
