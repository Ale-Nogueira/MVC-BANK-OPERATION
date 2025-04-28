from typing import List
from sqlalchemy import REAL
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.interfaces.bank_interface import BankInterface


class BankRepository(BankInterface):
    def __init__(self,db_connection) -> None:
        self.__db_connection = db_connection

    def list_pessoa_fisica(self) -> List[PessoaFisicaTable]:
        with self.__db_connection as database:
            try:
                pessoa_fisica = database.session.query(PessoaFisicaTable).all()
                return pessoa_fisica
            except NoResultFound:
                return []

    def insert_pessoa_fisica(self,renda_mensal: REAL, idade: int, nome_completo: str, celular: str, email: str, categoria: str, saldo: REAL) -> None:
        with self.__db_connection as database:
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
                database.session.add(person_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_person_fisica(self, person_id: int) -> PessoaFisicaTable:
        with self.__db_connection as database:
            try:
                person = (
                    database.session
                        .query(PessoaFisicaTable)
                        .filter(PessoaFisicaTable.id == person_id)
                        .with_entities(
                            PessoaFisicaTable.nome_completo,
                            PessoaFisicaTable.idade,
                            PessoaFisicaTable.saldo
                        )
                        .one()
                )
                return person
            except NoResultFound:
                return None

    def list_pessoa_juridica(self) -> List[PessoaJuridicaTable]:
        with self.__db_connection as database:
            try:
                pessoa_juridica = database.session.query(PessoaJuridicaTable).all()
                return pessoa_juridica
            except NoResultFound:
                return []

    def insert_pessoa_juridica(self,faturamento: REAL, idade: int, nome_fantasia: str, celular: str, email_corporativo: str, categoria: str, saldo: REAL) -> None:
        with self.__db_connection as database:
            try:
                person_data = PessoaJuridicaTable(
                    faturamento=faturamento,
                    idade=idade,
                    nome_fantasia=nome_fantasia,
                    celular=celular,
                    email_corporativo=email_corporativo,
                    categoria=categoria,
                    saldo=saldo
                )
                database.session.add(person_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_person_juridica(self, person_id: int) -> PessoaJuridicaTable:
        with self.__db_connection as database:
            try:
                person = (
                    database.session
                        .query(PessoaJuridicaTable)
                        .filter(PessoaJuridicaTable.id == person_id)
                        .with_entities(
                            PessoaJuridicaTable.nome_fantasia,
                            PessoaJuridicaTable.email_corporativo,
                            PessoaJuridicaTable.faturamento
                        )
                        .one()
                )
                return person
            except NoResultFound:
                return None
