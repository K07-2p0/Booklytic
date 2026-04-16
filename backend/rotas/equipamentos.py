from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import obter_bd
from models import Equipamento
from schemas import (
    EquipamentoCreate,
    EquipamentoUpdate,
    EquipamentoResponse
)

router = APIRouter()

@router.post("/equipamentos", response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_equipamento(equipamento: EquipamentoCreate, db: Session = Depends(obter_bd)):
    """Criar um novo equipamento na biblioteca tecnica"""
    novo_equipamento = Equipamento(**equipamento.model_dump())
    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)
    return novo_equipamento

@router.get("/equipamentos", response_model=List[EquipamentoResponse])
def listar_equipamentos(
    skip: int = 0,
    limit: int = 100,
    marca: Optional[str] = None,
    db: Session = Depends(obter_bd)
):
    """Listar todos os equipamentos com filtros opcionais"""
    query = db.query(Equipamento)

    if marca:
        query = query.filter(Equipamento.marca.ilike(f"%{marca}%"))

    equipamentos = query.offset(skip).limit(limit).all()
    return equipamentos

@router.get("/equipamentos/{equipamento_id}", response_model=EquipamentoResponse)
def obter_equipamento(equipamento_id: int, db: Session = Depends(obter_bd)):
    """Obter um equipamento especifico pelo ID"""
    equipamento = db.query(Equipamento).filter(Equipamento.id == equipamento_id).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento nao encontrado")
    return equipamento

@router.put("/equipamentos/{equipamento_id}", response_model=EquipamentoResponse)
def atualizar_equipamento(
    equipamento_id: int,
    equipamento_update: EquipamentoUpdate,
    db: Session = Depends(obter_bd)
):
    """Atualizar um equipamento existente"""
    equipamento = db.query(Equipamento).filter(Equipamento.id == equipamento_id).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento nao encontrado")

    update_data = equipamento_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(equipamento, field, value)

    db.commit()
    db.refresh(equipamento)
    return equipamento

@router.delete("/equipamentos/{equipamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipamento(equipamento_id: int, db: Session = Depends(obter_bd)):
    """Eliminar um equipamento da biblioteca"""
    equipamento = db.query(Equipamento).filter(Equipamento.id == equipamento_id).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento nao encontrado")

    db.delete(equipamento)
    db.commit()
    return None

@router.get("/equipamentos/pesquisa/{termo}", response_model=List[EquipamentoResponse])
def pesquisar_equipamentos(termo: str, db: Session = Depends(obter_bd)):
    """Pesquisar equipamentos por nome, marca ou modelo"""
    equipamentos = db.query(Equipamento).filter(
        (Equipamento.nome.ilike(f"%{termo}%")) |
        (Equipamento.marca.ilike(f"%{termo}%")) |
        (Equipamento.modelo.ilike(f"%{termo}%"))
    ).all()
    return equipamentos
