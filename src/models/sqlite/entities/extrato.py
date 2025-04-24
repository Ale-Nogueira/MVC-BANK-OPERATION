from sqlalchemy import Column, Integer, ForeignKey, REAL
from sqlalchemy.orm import relationship
from src.models.sqlite.setting.base import Base
from .pessoa_fisica import PessoaFisicaTable
from .pessoa_juridica import PessoaJuridicaTable

class ExtratoTable(Base):
    __tablename__ = "extrato"

    id = Column(Integer, primary_key=True)
    pessoa_fisica_id = Column(Integer, ForeignKey("pessoa_fisica.id"), nullable=True)
    pessoa_juridica_id = Column(Integer, ForeignKey("pessoa_juridica.id"), nullable=True)
    valor = Column(REAL)

ExtratoTable.pessoa_fisica = relationship("PessoaFisicaTable", back_populates="extratos")
ExtratoTable.pessoa_juridica = relationship("PessoaJuridicaTable", back_populates="extratos")
PessoaFisicaTable.extratos = relationship("ExtratoTable", back_populates="pessoa_fisica")
PessoaJuridicaTable.extratos = relationship("ExtratoTable", back_populates="pessoa_juridica")
