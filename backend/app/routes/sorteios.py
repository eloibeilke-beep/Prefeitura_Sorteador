from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import secrets
import hashlib
from datetime import datetime
from ..database import get_db
from ..models import Cupom, Sorteio, Usuario

router = APIRouter(prefix="/sorteios", tags=["sorteios"])

@router.post("/realizar-mensal")
def realizar_sorteio(mes: str, db: Session = Depends(get_db)):
    sorteio_existente = db.query(Sorteio).filter(Sorteio.mes_referencia == mes).first()
    if sorteio_existente:
        raise HTTPException(status_code=400, detail=f"O sorteio para o período {mes} já foi realizado.")

    cupons = db.query(Cupom).all()
    if not cupons:
        raise HTTPException(status_code=404, detail="Não há cupons cadastrados para realizar o sorteio.")

    vencedor_cupom = secrets.choice(cupons)
    usuario_vencedor = db.query(Usuario).filter(Usuario.id == vencedor_cupom.usuario_id).first()

    timestamp = datetime.now().isoformat()
    dados_auditoria = f"{timestamp}-{vencedor_cupom.numero_cupom}-{usuario_vencedor.cpf}"
    hash_auditoria = hashlib.sha256(dados_auditoria.encode()).hexdigest()

    novo_sorteio = Sorteio(
        mes_referencia=mes,
        cupom_vencedor_id=vencedor_cupom.id,
        hash_auditoria=hash_auditoria
    )
    db.add(novo_sorteio)
    db.commit()
    db.refresh(novo_sorteio)

    return {
        "resultado": "Sorteio realizado com sucesso!",
        "ganhador": usuario_vencedor.nome,
        "cpf_parcial": f"***.{usuario_vencedor.cpf[3:6]}.***-{usuario_vencedor.cpf[9:]}",
        "cupom_premiado": vencedor_cupom.numero_cupom,
        "hash_auditoria": hash_auditoria,
        "data": novo_sorteio.data_sorteio
    }

@router.get("/historico")
def listar_historico(db: Session = Depends(get_db)):
    return db.query(Sorteio).order_by(Sorteio.data_sorteio.desc()).all()
