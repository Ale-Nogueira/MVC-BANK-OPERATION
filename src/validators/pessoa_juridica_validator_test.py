from .pessoa_juridica_validator import saque_pessoa_juridica_validator

class MockRequest:
    def __init__(self, body) -> None:
        self.body = body

def test_saque_pessoa_fisica_validator():
    request = MockRequest({
        "person_id": 1,
        "valor": 1000

    })

    saque_pessoa_juridica_validator(request)
