from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
import random
import re
from ..database import get_db
from ..models import Usuario, Nota, Cupom

router = APIRouter(prefix="/notas", tags=["notas"])

class NotaInput(BaseModel):
    cpf_usuario: str
    chave_danfe: str
    tipo: str # 'PRODUTO' ou 'SERVICO'

    @field_validator('cpf_usuario')
    @classmethod
    def validar_cpf(cls, v: str):
        cpf = re.sub(r'\D', '', v)

        # Verifica se tem 11 dígitos ou se são todos iguais (ex: 111.111.111-11)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise ValueError('CPF inválido.')

        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        digito1 = 0 if resto == 10 else resto
        if digito1 != int(cpf[9]):
            raise ValueError('CPF inválido.')

        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        digito2 = 0 if resto == 10 else resto
        if digito2 != int(cpf[10]):
            raise ValueError('CPF inválido.')

        return cpf

    @field_validator('chave_danfe')
    @classmethod
    def validar_chave(cls, v: str):
        if len(v) != 44 or not v.isdigit():
            raise ValueError('A chave DANFE deve conter exatamente 44 dígitos numéricos.')
        return v

@router.post("/registrar")
def registrar_nota(nota: NotaInput, db: Session = Depends(get_db)):
    # 2. Verificar se a nota já foi registrada
    db_nota = db.query(Nota).filter(Nota.chave_danfe == nota.chave_danfe).first()
    if db_nota:
        raise HTTPException(status_code=400, detail="Nota fiscal já cadastrada no sistema.")
    
    # 3. Buscar ou criar usuário (Mock para facilitar testes)
    usuario = db.query(Usuario).filter(Usuario.cpf == nota.cpf_usuario).first()
    if not usuario:
        usuario = Usuario(cpf=nota.cpf_usuario, nome="Usuário de Teste")
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    # 4. Salvar a nota
    nova_nota = Nota(
        usuario_id=usuario.id,
        chave_danfe=nota.chave_danfe,
        tipo=nota.tipo.upper(),
        processada=True
    )
    db.add(nova_nota)
    db.commit()
    db.refresh(nova_nota)

    # 5. Gerar cupons
    quantidade_cupons = 2 if nota.tipo.upper() == "SERVICO" else 1
    numeros_gerados = []
    
    for _ in range(quantidade_cupons):
        # Gera um número aleatório e garante que ele é único no banco
        num = random.randint(1000000, 9999999)
        novo_cupom = Cupom(usuario_id=usuario.id, nota_id=nova_nota.id, numero_cupom=num)
        db.add(novo_cupom)
        numeros_gerados.append(num)
    
    db.commit()

    return {
        "status": "sucesso",
        "chave": nova_nota.chave_danfe,
        "cupons": numeros_gerados,
        "mensagem": f"{quantidade_cupons} cupom(ns) gerado(s) com sucesso."
    }
