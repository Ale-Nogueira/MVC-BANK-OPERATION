from typing import List
from sqlalchemy import REAL
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.entities.extrato import ExtratoTable

class PessoaFisicaRepository:
    def __init__(self, db_connection) -> None:
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

    def sacar_dinheiro(self, person_id: int, valor: REAL) -> str:
        with self.__db_connection as database:
            try:
                limite_saque = 2000

                pessoa_fisica = (
                    database.session
                        .query(PessoaFisicaTable)
                        .filter(PessoaFisicaTable.id == person_id)
                        .one_or_none()
                )

                if pessoa_fisica is None:
                    return "Cliente não encontrado"

                if pessoa_fisica.saldo < valor:
                    return "Saldo insuficiente!"

                if valor > limite_saque:
                    return f"O saque não pode exceder {limite_saque} para pessoa física."

                pessoa_fisica.saldo -= valor
                extrato = ExtratoTable(
                    pessoa_fisica_id=person_id,
                    valor=valor
                )
                database.session.add(extrato)
                database.session.commit()
                return f"Saque de {valor} realizado com sucesso! Saldo atual: {pessoa_fisica.saldo}"

            except Exception as exception:
                database.session.rollback()
                raise Exception("Erro ao realizar saque") from exception

    def realizar_extrato(self, person_id: int) -> str:
        with self.__db_connection as database:
            try:
                pessoa_fisica = (
                    database.session
                        .query(PessoaFisicaTable)
                        .filter(PessoaFisicaTable.id == person_id)
                        .one_or_none()
                )

                if pessoa_fisica is None:
                    return "Cliente não encontrado"

                extratos = (
                    database.session
                        .query(ExtratoTable)
                        .filter(ExtratoTable.pessoa_fisica_id == person_id)
                        .all()
                )

                historico = [f"Saque de R${e.valor:.2f}" for e in extratos]
                historico_texto = "\n".join(historico)

                return f"Extrato de saques:\n{historico_texto}\nSaldo atual: R${pessoa_fisica.saldo:.2f}"

            except Exception as exception:
                database.session.rollback()
                raise Exception("Erro ao consultar o extrato") from exception
