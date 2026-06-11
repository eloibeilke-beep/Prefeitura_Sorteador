from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
import requests
from bs4 import BeautifulSoup
import random
import re
from ..database import get_db
from ..models import Usuario, Nota, Cupom

router = APIRouter(prefix="/notas", tags=["notas"])

class NotaInput(BaseModel):
    cpf_usuario: str
    chave_danfe: str = None
    url_qr: str = None
    tipo: str  # 'PRODUTO' ou 'SERVICO'

    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v: str):
        if v.upper() not in ['PRODUTO', 'SERVICO']:
            raise ValueError('O tipo deve ser PRODUTO ou SERVICO')
        return v.upper()

    @field_validator('cpf_usuario')
    @classmethod
    def validar_cpf(cls, v: str):
        cpf = re.sub(r'\D', '', v)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise ValueError('CPF inválido.')

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        digito1 = 0 if resto == 10 else resto
        if digito1 != int(cpf[9]):
            raise ValueError('CPF inválido.')

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        digito2 = 0 if resto == 10 else resto
        if digito2 != int(cpf[10]):
            raise ValueError('CPF inválido.')

        return cpf

    @field_validator('chave_danfe')
    @classmethod
    def validar_chave(cls, v: str):
        if v and (len(v) != 44 or not v.isdigit()):
            raise ValueError('A chave DANFE deve conter exatamente 44 dígitos numéricos.')
        return v


def extrair_dados_sefaz_sc(url: str):
    """Raspa dados do portal SEFAZ/SC quando a chave não está na URL"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        chave_tag = soup.find("span", {"id": "lbl_ChaveAcesso"})
        chave = re.sub(r'\D', '', chave_tag.text) if chave_tag else None

        valor_tag = soup.find("span", {"id": "lbl_ValorTotal"})
        valor = float(valor_tag.text.replace(',', '.')) if valor_tag else 0.0

        return chave, valor
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
        return None, 0.0


@router.post("/registrar")
def registrar_nota(dados: NotaInput, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.cpf == dados.cpf_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if dados.url_qr and not dados.chave_danfe:
        chave, valor = extrair_dados_sefaz_sc(dados.url_qr)
        if not chave:
            raise HTTPException(status_code=400, detail="Não foi possível extrair a chave DANFE.")
        dados.chave_danfe = chave
    else:
        valor = 0.0

    nova_nota = Nota(
        usuario_id=usuario.id,
        chave_danfe=dados.chave_danfe,
        tipo=dados.tipo,
        valor=valor
    )
    db.add(nova_nota)
    db.commit()
    db.refresh(nova_nota)

    numero_cupom = random.randint(100000, 999999)
    novo_cupom = Cupom(
        usuario_id=usuario.id,
        nota_id=nova_nota.id,
        numero_cupom=numero_cupom
    )
    db.add(novo_cupom)
    db.commit()

    return {
        "mensagem": "Nota registrada com sucesso!",
        "cupom": numero_cupom,
        "valor": valor
    }
