from typing import List
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable

class PessoaJuridicaRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def list_pessoa_juridica(self) -> List[PessoaJuridicaTable]:
        with self.__db_connection as databse:
            try:
                pessoa_juridica = databse.session.query(PessoaJuridicaTable).all()
                return pessoa_juridica
            except NoResultFound:
                return []
