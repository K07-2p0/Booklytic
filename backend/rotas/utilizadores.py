from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from database import obter_bd
from models import Utilizador
from schemas import UtilizadorCreate, UtilizadorResponse, LoginRequest, LoginResponse

router = APIRouter()

# Configurar hashing de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/utilizadores", response_model=UtilizadorResponse, status_code=status.HTTP_201_CREATED)
def criar_utilizador(utilizador: UtilizadorCreate, db: Session = Depends(obter_bd)):
    """Criar um novo utilizador/tecnico"""
    # Verificar se email ja existe
    db_utilizador = db.query(Utilizador).filter(Utilizador.email == utilizador.email).first()
    if db_utilizador:
        raise HTTPException(status_code=400, detail="Email ja registado")

    # Criar novo utilizador com password hash
    novo_utilizador = Utilizador(
        nome=utilizador.nome,
        email=utilizador.email,
        password_hash=hash_password(utilizador.password),
        tipo=utilizador.tipo
    )
    db.add(novo_utilizador)
    db.commit()
    db.refresh(novo_utilizador)
    return novo_utilizador

@router.get("/utilizadores", response_model=List[UtilizadorResponse])
def listar_utilizadores(skip: int = 0, limit: int = 100, db: Session = Depends(obter_bd)):
    """Listar todos os utilizadores"""
    utilizadores = db.query(Utilizador).offset(skip).limit(limit).all()
    return utilizadores

@router.get("/utilizadores/{utilizador_id}", response_model=UtilizadorResponse)
def obter_utilizador(utilizador_id: int, db: Session = Depends(obter_bd)):
    """Obter um utilizador especifico pelo ID"""
    utilizador = db.query(Utilizador).filter(Utilizador.id == utilizador_id).first()
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador nao encontrado")
    return utilizador

@router.put("/utilizadores/{utilizador_id}", response_model=UtilizadorResponse)
def atualizar_utilizador(
    utilizador_id: int,
    utilizador_update: UtilizadorCreate,
    db: Session = Depends(obter_bd)
):
    """Atualizar um utilizador existente"""
    utilizador = db.query(Utilizador).filter(Utilizador.id == utilizador_id).first()
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador nao encontrado")

    # Verificar se o novo email ja existe
    if utilizador_update.email != utilizador.email:
        db_utilizador = db.query(Utilizador).filter(Utilizador.email == utilizador_update.email).first()
        if db_utilizador:
            raise HTTPException(status_code=400, detail="Email ja registado")

    utilizador.nome = utilizador_update.nome
    utilizador.email = utilizador_update.email
    utilizador.tipo = utilizador_update.tipo

    db.commit()
    db.refresh(utilizador)
    return utilizador

@router.delete("/utilizadores/{utilizador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_utilizador(utilizador_id: int, db: Session = Depends(obter_bd)):
    """Eliminar um utilizador"""
    utilizador = db.query(Utilizador).filter(Utilizador.id == utilizador_id).first()
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador nao encontrado")

    db.delete(utilizador)
    db.commit()
    return None

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(obter_bd)):
    """Autenticar um utilizador"""
    utilizador = db.query(Utilizador).filter(Utilizador.email == credentials.email).first()

    if not utilizador or not verify_password(credentials.password, utilizador.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou password incorretos"
        )

    # Nota: Em producao, deveria gerar um JWT token aqui
    # Para simplificar, estamos a retornar um token dummy
    import secrets
    token = secrets.token_urlsafe(32)

    return {"access_token": token, "token_type": "bearer"}
