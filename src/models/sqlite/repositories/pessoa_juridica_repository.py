from sqlalchemy import REAL
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.entities.extrato import ExtratoTable
from src.models.sqlite.interfaces.cliente_interface import ClienteInterface


class PessoaJuridicaRepository(ClienteInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

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

                saques = [{"valor": float(e.valor)} for e in extratos]

                return {
                    "saques": saques,
                    "saldo_atual": float(pessoa_juridica.saldo)
                }

            except Exception as exception:
                database.session.rollback()
                raise Exception("Erro ao consultar o extrato") from exception
