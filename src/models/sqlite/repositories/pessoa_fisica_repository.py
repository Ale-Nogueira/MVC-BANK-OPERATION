from typing import List
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class PessoaFisicaRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def list_pessoa_fisica(self) -> List[PessoaFisicaTable]:
        with self.__db_connection as databse:
            try:
                pessoa_fisica = databse.session.query(PessoaFisicaTable).all()
                return pessoa_fisica
            except NoResultFound:
                return []
