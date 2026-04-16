from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# Schemas para Utilizadores
class UtilizadorBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    tipo: str = Field(default="tecnico", pattern="^(admin|tecnico)$")

class UtilizadorCreate(UtilizadorBase):
    password: str = Field(..., min_length=8)

class UtilizadorResponse(UtilizadorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas para Marcacoes
class MarcacaoBase(BaseModel):
    cliente_nome: str = Field(..., min_length=2, max_length=100)
    cliente_email: EmailStr
    cliente_telefone: Optional[str] = Field(None, max_length=20)
    data_hora: datetime
    descricao: Optional[str] = None
    estado: str = Field(default="pendente", pattern="^(pendente|confirmada|cancelada|concluida)$")

class MarcacaoCreate(MarcacaoBase):
    tecnico_id: Optional[int] = None

class MarcacaoUpdate(BaseModel):
    cliente_nome: Optional[str] = Field(None, min_length=2, max_length=100)
    cliente_email: Optional[EmailStr] = None
    cliente_telefone: Optional[str] = Field(None, max_length=20)
    data_hora: Optional[datetime] = None
    descricao: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(pendente|confirmada|cancelada|concluida)$")
    tecnico_id: Optional[int] = None

class MarcacaoResponse(MarcacaoBase):
    id: int
    tecnico_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class MarcacaoComTecnico(MarcacaoResponse):
    tecnico: Optional[UtilizadorResponse] = None

# Schemas para Equipamentos
class EquipamentoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    marca: Optional[str] = Field(None, max_length=50)
    modelo: Optional[str] = Field(None, max_length=50)
    numero_serie: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = None

class EquipamentoCreate(EquipamentoBase):
    pass

class EquipamentoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    marca: Optional[str] = Field(None, max_length=50)
    modelo: Optional[str] = Field(None, max_length=50)
    numero_serie: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = None

class EquipamentoResponse(EquipamentoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schema para Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
