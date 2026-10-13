import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.concurrency import run_in_threadpool

from app.esquemas import RequisicaoEmail, RespostaEmail
from app.servicos import ServicoCriptografia, ServicoEmail

registrador = logging.getLogger("GatewayEmailSeguro.Rotas")
roteador = APIRouter(prefix="/api/v1", tags=["Email"])

@roteador.post(
    "/enviar-email",
    response_model=RespostaEmail,
    status_code=status.HTTP_200_OK,
    summary="Envio de mensagem segura"
)
async def rota_enviar_email(dados: RequisicaoEmail):
    try:
        corpo_criptografado = await run_in_threadpool(ServicoCriptografia.criptografar_pgp_e2ee, dados.conteudo)
        await run_in_threadpool(ServicoEmail.enviar_mensagem_smtp, dados, corpo_criptografado)

        registrador.info(f"E-mail entregue com sucesso para {dados.email_destino}")
        return RespostaEmail(
            status="sucesso",
            mensagem="Mensagem processada e enviada com sucesso.",
            destinatario=dados.email_destino
        )
    except ValueError as erro_config:
        registrador.error(f"Erro de configuração: {erro_config}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Serviço indisponível devido a um erro interno de configuração."
        )
    except Exception as erro_inesperado:
        # Grava os detalhes nos logs para você depurar, mas não vaza rastros ao cliente
        registrador.error(f"Falha ao enviar e-mail via SMTP: {erro_inesperado}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Não foi possível entregar a mensagem através do servidor SMTP."
        )