from typing import Optional
from pydantic_settings import BaseSettings

class Configuracoes(BaseSettings):
    servidor_smtp: str = "smtp.gmail.com"
    porta_smtp: int = 465
    usuario_smtp: str = ""
    senha_smtp: str = ""
    gnupg_home: Optional[str] = None
    chave_recipiente_pgp: Optional[str] = None
    origens_cors: str = "http://127.0.0.1:8000,http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"

configuracoes = Configuracoes()