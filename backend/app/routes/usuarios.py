from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

class UsuarioCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str

@router.post("/cadastro")
def cadastrar_usuario(user: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.cpf == user.cpf).first()
    if existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    
    novo_usuario = Usuario(nome=user.nome, cpf=user.cpf, telefone=user.telefone)
    db.add(novo_usuario)
    db.commit()
    return {"mensagem": "Usuário cadastrado com sucesso!"}

@router.get("/{cpf}/cupons")
def listar_cupons(cpf: str, db: Session = Depends(get_db)):
    # Busca o usuário pelo CPF
    usuario = db.query(Usuario).filter(Usuario.cpf == cpf).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou ainda não possui notas cadastradas.")

    return {
        "nome": usuario.nome,
        "cpf": usuario.cpf,
        "total_cupons": len(usuario.cupons),
        "cupons": [
            {"numero": c.numero_cupom, "data_geracao": c.criado_em} for c in usuario.cupons
        ]
    }