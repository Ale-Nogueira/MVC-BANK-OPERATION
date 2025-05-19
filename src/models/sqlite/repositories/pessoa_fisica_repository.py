from sqlalchemy import REAL
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.entities.extrato import ExtratoTable
from src.models.sqlite.interfaces.cliente_interface import ClienteInterface

class PessoaFisicaRepository(ClienteInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

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

                if not extratos:
                    return f"Sem movimentação para o cliente {person_id}."

                saques = [{"valor": float(e.valor)} for e in extratos]

                return {
                    "saques": saques,
                    "saldo_atual": float(pessoa_fisica.saldo)
                }

            except Exception as exception:
                database.session.rollback()
                raise Exception("Erro ao consultar o extrato") from exception
