from pydantic import BaseModel, ValidationError
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

def saque_pessoa_fisica_validator(http_request: HttpRequest) -> None:

    class BodyData(BaseModel):
        person_id: int
        valor: int

    try:
        BodyData(**http_request.body)
    except ValidationError as e:
        raise HttpUnprocessableEntityError(e.errors()) from e
