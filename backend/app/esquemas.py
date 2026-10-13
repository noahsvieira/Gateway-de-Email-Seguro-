import re
from pydantic import BaseModel, EmailStr, Field, field_validator

class RequisicaoEmail(BaseModel):
    email_destino: EmailStr = Field(..., description="E-mail de destino válido")
    assunto: str = Field(
        ..., 
        min_length=3, 
        max_length=150, 
        pattern=r"^[^\r\n]+$",
        description="Assunto protegido contra Header Injection"
    )
    conteudo: str = Field(
        ..., 
        min_length=5, 
        max_length=5000, 
        description="Conteúdo da mensagem"
    )

    @field_validator('conteudo')
    def validar_protecao_anti_phishing(cls, valor: str) -> str:
        """
        Bloqueia padrões óbvios de phishing ou tentativas de injetar textos 
        associados a golpes de engenharia social.
        """
        palavras_proibidas = [
            "confirme sua senha", 
            "atualize seus dados bancarios", 
            "clique aqui imediatamente para nao perder o acesso"
        ]
        conteudo_minusculo = valor.lower()
        
        for termo in palavras_proibidas:
            if termo in conteudo_minusculo:
                raise ValueError("Conteúdo bloqueado pelas políticas de segurança anti-phishing da organização.")
                
        return valor

    @field_validator('assunto')
    def validar_assunto_seguro(cls, valor: str) -> str:
        return valor.strip()

class RespostaEmail(BaseModel):
    status: str
    mensagem: str
    destinatario: str