from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, REAL
from src.models.sqlite.setting.base import Base

class ExtratoTable(Base):
    __tablename__ = "extrato"

    id = Column(Integer, primary_key=True)
    pessoa_fisica_id = Column(Integer, ForeignKey("pessoa_fisica.id"), nullable=True)
    pessoa_juridica_id = Column(Integer, ForeignKey("pessoa_juridica.id"), nullable=True)
    valor = Column(REAL)

    pessoa_fisica = relationship("PessoaFisicaTable", back_populates="extratos")
    pessoa_juridica = relationship("PessoaJuridicaTable", back_populates="extratos")
