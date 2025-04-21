from sqlalchemy import Column, String, BIGINT, REAL
from src.models.sqlite.setting.base import Base


class PessoaJuridica(Base):
    __tablename__ = "pessoa juridica"

    id = Column(BIGINT, primary_key=True)
    faturamento = Column(REAL, nullable=False)
    idade = Column(BIGINT, nullable=False)
    nome_fantasia = Column(String, nullabe=False)
    celular = Column(String, nullable=False)
    email_corporativo = Column(String, nullable=False)
    categoria = Column(String)
    saldo = Column(REAL)

    def __repr__(self):
        return f"pessoa juridica [name={self.nome_fantasia}, faturamento={self.faturamento}]"
