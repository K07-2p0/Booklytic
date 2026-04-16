from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Utilizador(Base):
    __tablename__ = "utilizadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    tipo = Column(String(20), default="tecnico")  # admin, tecnico
    created_at = Column(DateTime, default=datetime.utcnow)

    marcacoes = relationship("Marcacao", back_populates="tecnico")

class Marcacao(Base):
    __tablename__ = "marcacoes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String(100), nullable=False)
    cliente_email = Column(String(100), nullable=False)
    cliente_telefone = Column(String(20))
    data_hora = Column(DateTime, nullable=False)
    descricao = Column(Text)
    estado = Column(String(20), default="pendente")  # pendente, confirmada, cancelada, concluida
    tecnico_id = Column(Integer, ForeignKey("utilizadores.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    tecnico = relationship("Utilizador", back_populates="marcacoes")

class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    marca = Column(String(50))
    modelo = Column(String(50))
    numero_serie = Column(String(50))
    descricao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
