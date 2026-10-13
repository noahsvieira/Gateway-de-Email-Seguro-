import time
import logging
from collections import defaultdict
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.configuracao import configuracoes
from app.rotas import roteador

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
)

app = FastAPI(
    title="Portal de Comunicação Seguro",
    description="Microserviço corporativo com E2EE e transporte SMTPS.",
    version="1.0.0"
)

# --- 1. MIDDLEWARE: Rate Limiting (Proteção contra Anti-Spam e DoS) ---
historico_requisicoes = defaultdict(list)
LIMITE_REQUISICOES = 5
JANELA_TEMPO_SEGUNDOS = 60

@app.middleware("http")
async def limitar_taxa_requisicoes(request: Request, call_next):
    if request.url.path == "/api/v1/enviar-email" and request.method == "POST":
        ip_cliente = request.client.host if request.client else "desconhecido"
        agora = time.time()
        
        historico_requisicoes[ip_cliente] = [
            t for t in historico_requisicoes[ip_cliente] if agora - t < JANELA_TEMPO_SEGUNDOS
        ]
        
        if len(historico_requisicoes[ip_cliente]) >= LIMITE_REQUISICOES:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Erro [HTTP 429]: Limite de envios excedido. Tente novamente em 1 minuto."
            )
            
        historico_requisicoes[ip_cliente].append(agora)

    response = await call_next(request)
    return response

# --- 2. MIDDLEWARE: Cabeçalhos de Segurança (Security Headers OWASP) ---
@app.middleware("http")
async def adicionar_cabecalhos_seguranca(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# --- 3. MIDDLEWARE: CORS Restrito ---
origens_permitidas = [origem.strip() for origem in configuracoes.origens_cors.split(",") if origem.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# --- 4. ROTAS E FRONTEND ---
app.include_router(roteador)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")