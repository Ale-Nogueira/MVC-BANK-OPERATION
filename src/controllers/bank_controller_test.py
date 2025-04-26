from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from .bank_controller import BankListController

class MockBankRepository:
    def list_pessoa_fisica(self):
        return [
            PessoaFisicaTable(nome_completo="fulano de tal", idade=18, email="fulano@email.com", id=1),
            PessoaFisicaTable(nome_completo="ciclano de tal", idade=21, email="ciclano@email.com", id=2)
        ]

def test_list_pessoa_fisica():
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
