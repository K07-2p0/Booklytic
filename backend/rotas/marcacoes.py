from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import obter_bd
from models import Marcacao, Utilizador
from schemas import MarcacaoCreate, MarcacaoUpdate, MarcacaoComTecnico

router = APIRouter()

@router.post("/marcacoes", response_model=MarcacaoComTecnico, status_code=status.HTTP_201_CREATED)
def criar_marcacao(marcacao: MarcacaoCreate, db: Session = Depends(obter_bd)):
    """Criar uma nova marcacao"""
    nova_marcacao = Marcacao(**marcacao.model_dump())
    db.add(nova_marcacao)
    db.commit()
    db.refresh(nova_marcacao)
    return nova_marcacao

@router.get("/marcacoes", response_model=List[MarcacaoComTecnico])
def listar_marcacoes(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(obter_bd)
):
    """Listar todas as marcacoes com filtros opcionais"""
    query = db.query(Marcacao)

    if estado:
        query = query.filter(Marcacao.estado == estado)

    marcacoes = query.offset(skip).limit(limit).all()
    return marcacoes

@router.get("/marcacoes/{marcacao_id}", response_model=MarcacaoComTecnico)
def obter_marcacao(marcacao_id: int, db: Session = Depends(obter_bd)):
    """Obter uma marcacao especifica pelo ID"""
    marcacao = db.query(Marcacao).filter(Marcacao.id == marcacao_id).first()
    if not marcacao:
        raise HTTPException(status_code=404, detail="Marcacao nao encontrada")
    return marcacao

@router.put("/marcacoes/{marcacao_id}", response_model=MarcacaoComTecnico)
def atualizar_marcacao(
    marcacao_id: int,
    marcacao_update: MarcacaoUpdate,
    db: Session = Depends(obter_bd)
):
    """Atualizar uma marcacao existente"""
    marcacao = db.query(Marcacao).filter(Marcacao.id == marcacao_id).first()
    if not marcacao:
        raise HTTPException(status_code=404, detail="Marcacao nao encontrada")

    update_data = marcacao_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(marcacao, field, value)

    db.commit()
    db.refresh(marcacao)
    return marcacao

@router.delete("/marcacoes/{marcacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_marcacao(marcacao_id: int, db: Session = Depends(obter_bd)):
    """Eliminar uma marcacao"""
    marcacao = db.query(Marcacao).filter(Marcacao.id == marcacao_id).first()
    if not marcacao:
        raise HTTPException(status_code=404, detail="Marcacao nao encontrada")

    db.delete(marcacao)
    db.commit()
    return None

@router.get("/marcacoes/tecnico/{tecnico_id}", response_model=List[MarcacaoComTecnico])
def listar_marcacoes_por_tecnico(tecnico_id: int, db: Session = Depends(obter_bd)):
    """Listar todas as marcacoes de um tecnico especifico"""
    tecnico = db.query(Utilizador).filter(Utilizador.id == tecnico_id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="Tecnico nao encontrado")

    marcacoes = db.query(Marcacao).filter(Marcacao.tecnico_id == tecnico_id).all()
    return marcacoes
