from typing import List
from sqlalchemy import REAL
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.entities.extrato import ExtratoTable
from src.models.sqlite.interfaces.cliente_interface import ClienteInterface


class PessoaJuridicaRepository(ClienteInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

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

    def get_person(self, person_id: int) -> PessoaJuridicaTable:
        with self.__db_connection as database:
            try:
                person = (
                    database.session
                        .query(PessoaJuridicaTable)
                        .filter(PessoaJuridicaTable.id == person_id)
                        .with_entities(
                            PessoaJuridicaTable.nome_fantasia,
                            PessoaJuridicaTable.idade,
                            PessoaJuridicaTable.faturamento
                        )
                        .one()
                )
                return person
            except NoResultFound:
                return None

    def sacar_dinheiro(self, person_id: int, valor: REAL) -> str:
        with self.__db_connection as database:
            try:
                limite_saque = 10000

                pessoa_juridica = (
                    database.session
                        .query(PessoaJuridicaTable)
                        .filter(PessoaJuridicaTable.id == person_id)
                        .one_or_none()
                )

                if pessoa_juridica is None:
                    return "Empresa não encontrada"

                if pessoa_juridica.saldo < valor:
                    return "Saldo insuficiente!"

                if valor > limite_saque:
                    return f"O saque não pode exceder {limite_saque} para pessoa juridica."

                pessoa_juridica.saldo -= valor
                extrato = ExtratoTable(
                    pessoa_juridica_id=person_id,
                    valor=valor
                )
                database.session.add(extrato)
                database.session.commit()
                return f"Saque de {valor} realizado com sucesso! Saldo atual: {pessoa_juridica.saldo}"

            except Exception as exception:
                database.session.rollback()
                raise Exception("Erro ao realizar saque") from exception

    def realizar_extrato(self, person_id: int) -> str:
        with self.__db_connection as database:
            try:
                pessoa_juridica = (
                    database.session
                        .query(PessoaJuridicaTable)
                        .filter(PessoaJuridicaTable.id == person_id)
                        .one_or_none()
                )

                if pessoa_juridica is None:
                    return "Empresa não encontrada"

                extratos = (
                    database.session
                        .query(ExtratoTable)
                        .filter(ExtratoTable.pessoa_juridica_id == person_id)
                        .all()
                )

                if not extratos:
                    return f"Sem movimentação para a empresa {person_id}."

                historico = [f"Saque de R${e.valor:.2f}" for e in extratos]
                historico_texto = "\n".join(historico)

                return f"Extrato de saques:\n{historico_texto}\nSaldo atual: R${pessoa_juridica.saldo:.2f}"

            except Exception as exception:
                database.session.rollback()
                raise Exception("Erro ao consultar o extrato") from exception
