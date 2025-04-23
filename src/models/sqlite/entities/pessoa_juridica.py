from sqlalchemy import Column, String, BIGINT, REAL
from sqlalchemy.orm import relationship
from src.models.sqlite.setting.base import Base
from .extrato import ExtratoTable

class PessoaJuridicaTable(Base):
    __tablename__ = "pessoa_juridica"

    id = Column(BIGINT, primary_key=True)
    faturamento = Column(REAL, nullable=False)
    idade = Column(BIGINT, nullable=False)
    nome_fantasia = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email_corporativo = Column(String, nullable=False)
    categoria = Column(String)
    saldo = Column(REAL)
    extratos = relationship(ExtratoTable, back_populates="pessoa_juridica")

    def __repr__(self):
        return f"pessoa_juridica [name={self.nome_fantasia}, faturamento={self.faturamento}]"
