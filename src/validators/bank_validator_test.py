from .bank_validator import insert_pessoa_fisica_validator, insert_pessoa_juridica_validator

class MockRequest:
    def __init__(self, body) -> None:
        self.body = body

def test_bank_fisica_validator():
    request = MockRequest({
        "renda_mensal": 3000,
        "idade": 25,
        "nome_completo": "fulano de tal",
        "celular": "199555221",
        "email": "fulano@email.com",
        "categoria": "categoria A",
        "saldo": 2500
    })

    insert_pessoa_fisica_validator(request)

def test_bank_juridica_validator():
    request = MockRequest({
        "faturamento": 100000,
        "idade": 5,
        "nome_fantasia": "empresa x",
        "celular": "199555221",
        "email_corporativo": "empresax@email.com",
        "categoria": "categoria A",
        "saldo": 50000
    })

    insert_pessoa_juridica_validator(request)
