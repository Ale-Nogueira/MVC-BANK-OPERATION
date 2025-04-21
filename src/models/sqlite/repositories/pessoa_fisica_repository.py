from typing import List
from sqlalchemy import REAL
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

    def insert_pessoa_fisica(self,renda_mensal: REAL, idade: int, nome_completo: str, celular: str, email: str, categoria: str, saldo: REAL) -> None:
        with self.__db_connection as databse:
            try:
                person_data = PessoaFisicaTable(
                    renda_mensal=renda_mensal,
                    idade=idade,
                    nome_completo=nome_completo,
                    celular=celular,
                    email=email,
                    categoria=categoria,
                    saldo=saldo
                )
                databse.session.add(person_data)
                databse.session.commit()
            except Exception as exception:
                databse.session.rollback()
                raise exception

    def get_person(self, person_id: int) -> PessoaFisicaTable:
        with self.__db_connection as database:
            try:
                person = (
                    database.session
                        .query(PessoaFisicaTable)
                        .filter(PessoaFisicaTable.id == person_id)
                        .with_entities(
                            PessoaFisicaTable.nome_completo,
                            PessoaFisicaTable.idade,
                            PessoaFisicaTable.renda_mensal
                        )
                        .one()
                )
                return person
            except NoResultFound:
                return None
