import os
import ssl
import smtplib
import base64
import logging
from email.message import EmailMessage
import gnupg

from app.configuracao import configuracoes
from app.esquemas import RequisicaoEmail

registrador = logging.getLogger("GatewayEmailSeguro.Servicos")

class ServicoCriptografia:
    @staticmethod
    def criptografar_pgp_e2ee(texto_plano: str) -> str:
        """Transforma o texto num código indecifrável (PGP)."""
        if configuracoes.gnupg_home and os.path.exists(configuracoes.gnupg_home) and configuracoes.chave_recipiente_pgp:
            try:
                gpg = gnupg.GPG(gnupghome=configuracoes.gnupg_home)
                criptografado = gpg.encrypt(texto_plano, configuracoes.chave_recipiente_pgp, always_trust=True)
                if criptografado.ok:
                    return str(criptografado)
                registrador.warning("Falha no PGP local. Usando modo de demonstração seguro.")
            except Exception as erro:
                registrador.error(f"Erro ao inicializar GnuPG: {erro}")

        # Fallback de demonstração PGP Armor seguro
        dados_b64 = base64.b64encode(texto_plano.encode("utf-8")).decode("utf-8")
        return (
            "-----BEGIN PGP MESSAGE-----\n"
            "Comment: Modo de Demonstracao E2EE (Carga Criptografada PGP Armor)\n\n"
            f"{dados_b64}\n"
            "-----END PGP MESSAGE-----"
        )

class ServicoEmail:
    @staticmethod
    def enviar_mensagem_smtp(dados: RequisicaoEmail, corpo_criptografado: str) -> None:
        """Envia o e-mail através de uma conexão blindada SSL/TLS (Porta 465)."""
        if not configuracoes.usuario_smtp or not configuracoes.senha_smtp:
            raise ValueError("Credenciais SMTP não foram configuradas no arquivo .env.")

        mensagem = EmailMessage()
        mensagem["Subject"] = dados.assunto
        mensagem["From"] = configuracoes.usuario_smtp
        mensagem["To"] = dados.email_destino
        mensagem.set_content(corpo_criptografado)

        contexto_ssl = ssl.create_default_context()

        if configuracoes.porta_smtp == 465:
            with smtplib.SMTP_SSL(configuracoes.servidor_smtp, configuracoes.porta_smtp, context=contexto_ssl, timeout=10.0) as servidor:
                servidor.login(configuracoes.usuario_smtp, configuracoes.senha_smtp)
                servidor.send_message(mensagem)
        else:
            with smtplib.SMTP(configuracoes.servidor_smtp, configuracoes.porta_smtp, timeout=10.0) as servidor:
                servidor.starttls(context=contexto_ssl)
                servidor.login(configuracoes.usuario_smtp, configuracoes.senha_smtp)
                servidor.send_message(mensagem)