from sqlalchemy import Column, String, BIGINT, REAL
from src.models.sqlite.setting.base import Base

class PessoaFisicaTable(Base):
    __tablename__ = "pessoa_fisica"

    id = Column(BIGINT, primary_key=True)
    renda_mensal = Column(REAL, nullable=False)
    idade = Column(BIGINT, nullable=False)
    nome_completo = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email = Column(String, nullable=False)
    categoria = Column(String)
    saldo = Column(REAL)

    def __repr__(self):
        return f"pessoa_fisica [name={self.nome_completo}, renda={self.renda_mensal}]"
