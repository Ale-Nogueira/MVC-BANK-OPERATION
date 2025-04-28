from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from .bank_controller import BankListPessoaFisicaController
from .bank_controller import BankInsertPessoaFisicaController

class MockBankRepository:
    def list_pessoa_fisica(self):
        return [
            PessoaFisicaTable(nome_completo="fulano de tal", idade=18, email="fulano@email.com", id=1),
            PessoaFisicaTable(nome_completo="ciclano de tal", idade=21, email="ciclano@email.com", id=2)
        ]

    def insert_pessoa_fisica(self, renda_mensal: int, idade: int, nome_completo: str, celular: str, email: str, categoria: str, saldo: int) -> None:
        pass


def test_list_pessoa_fisica():
    controller = BankListPessoaFisicaController(MockBankRepository())
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

def test_insert_pessoa_fisica():
    person_info = {
        "renda_mensal": 5000,
        "idade": 25,
        "nome_completo": "fulano de tal",
        "celular": "99885544",
        "email": "fulano@email.com",
        "categoria": "categoria A",
        "saldo": 3000
    }

    controller = BankInsertPessoaFisicaController(MockBankRepository())
    response =  controller.insert(person_info)

    assert response["data"]["type"] == "Pessoa Fisica"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == person_info
