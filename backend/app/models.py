from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Boolean, BigInteger, func
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200))
    cpf = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(20))
    criado_em = Column(DateTime, server_default=func.now())
    
    notas = relationship("Nota", back_populates="usuario")
    cupons = relationship("Cupom", back_populates="usuario")

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    chave_danfe = Column(String(44), unique=True, nullable=False)
    tipo = Column(String(20), nullable=False)
    valor = Column(DECIMAL(10, 2))
    data_emissao = Column(DateTime)
    processada = Column(Boolean, default=False)
    criado_em = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="notas")
    cupons = relationship("Cupom", back_populates="nota")

class Cupom(Base):
    __tablename__ = "cupons"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nota_id = Column(Integer, ForeignKey("notas.id"))
    numero_cupom = Column(BigInteger, unique=True, nullable=False)
    criado_em = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="cupons")
    nota = relationship("Nota", back_populates="cupons")

class Sorteio(Base):
    __tablename__ = "sorteios"
    id = Column(Integer, primary_key=True, index=True)
    data_sorteio = Column(DateTime, server_default=func.now())
    mes_referencia = Column(String(20))
    cupom_vencedor_id = Column(Integer, ForeignKey("cupons.id"))
    hash_auditoria = Column(String(64))

    cupom_vencedor = relationship("Cupom")
