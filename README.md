# Secure Mail Gateway 🛡️

Microsserviço de gateway de e-mails corporativos focado em Cibersegurança, Arquitetura Defensiva e Criptografia de Ponta a Ponta (E2EE). Desenvolvido para portfólio, evoluindo de um formulário simples para uma aplicação backend robusta.

## Recursos de Segurança

* Validação Anti-Phishing: Filtros estritos em Pydantic para bloquear entradas maliciosas e engenharia social.
* Blindagem contra Header Injection: Proteção rigorosa contra injeção de cabeçalhos SMTP.
* Criptografia E2EE (PGP Armor): Encapsulamento e criptografia de mensagens antes do transporte.
* Error Masking: Ocultação de detalhes internos de exceção para evitar vazamento de dados.
* Interface Corporativa Sanitizada: Protegida contra vulnerabilidades web.

## Tecnologias

* Python 3.10+
* FastAPI & Uvicorn
* Pydantic v2 & Pydantic Settings
* GnuPG / OpenPGP (python-gnupg)
* Ethereal Email (Ambiente SMTP Sandbox)
* Pytest & HTTPX (Testes automatizados)

## Como rodar o projeto

git clone https://github.com/noahsvieira/Gateway-de-Email-Seguro-
cd gateway-email-seguro
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requisitos.txt

Crie um arquivo .env dentro da pasta backend/ preenchendo com as suas credenciais do Ethereal:

SERVIDOR_SMTP=smtp.ethereal.email
PORTA_SMTP=587
USUARIO_SMTP=seu_usuario@ethereal.email
SENHA_SMTP=sua_senha
ORIGENS_CORS=http://127.0.0.1:8000,http://localhost:8000

Depois, inicie o servidor:

cd backend
python -m uvicorn main:app --reload

A interface do usuário fica disponível em http://127.0.0.1:8000.

## Testes Automatizados

Para rodar os testes da API:

pytest

## Licença

Este projeto está sob a licença MIT.