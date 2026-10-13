# Secure Mail Gateway - Gateway de E-mail Seguro e Criptografado

API própria e microserviço corporativo, construído em Python com FastAPI, que processa o envio de mensagens confidenciais com criptografia de ponta a ponta (E2EE / PGP Armor) e transporte protegido via SMTPS (TLS).

Projeto de portfólio em cibersegurança e desenvolvimento backend, focado em aplicação prática de defesa em profundidade (*Defense in Depth*) e conformidade com boas práticas OWASP, utilizando ambiente sandbox de e-mail (Ethereal) sem envio de mensagens reais para a internet.

---

## Sumário
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Endpoints](#endpoints)
- [Demonstração](#demonstração)
- [Licença](#licença)
- [Aviso de segurança](#aviso-de-segurança)

---

## Funcionalidades
- Envio de e-mails confidenciais com criptografia PGP Armor no corpo da mensagem
- Transporte seguro de mensagens via protocolo SMTPS (TLS/SSL)
- Proteção contra injeção de cabeçalho (*Email Header Injection*)
- Proteção anti-phishing com validação proativa de conteúdo e engenharia social
- Limitação de taxa de requisições por IP (*Rate Limiting*) contra ataques de DoS e spam
- Proteção via cabeçalhos HTTP de segurança (*Security Headers* OWASP)
- Ocultação de detalhes internos de exceção (*Error Masking*) para evitar vazamento de dados
- Interface web corporativa neutra e sanitizada contra Cross-Site Scripting (XSS)

---

## Tecnologias
- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic v2 & Pydantic Settings
- GnuPG / OpenPGP (python-gnupg)
- Ethereal Email (Ambiente SMTP Sandbox)
- Pytest & HTTPX (Testes automatizados)
- HTML5, CSS3 e JavaScript (Vanilla)

---

## Como rodar o projeto

```bash
git clone <link-do-seu-repositorio>
cd gateway-email-seguro
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requisitos.txt

Crie o arquivo .env dentro da pasta backend/ preenchendo com suas próprias chaves do Ethereal:

SERVIDOR_SMTP=smtp.ethereal.email
PORTA_SMTP=587
USUARIO_SMTP=seu_usuario@ethereal.email
SENHA_SMTP=sua_senha
ORIGENS_CORS=[http://127.0.0.1:8000](http://127.0.0.1:8000),http://localhost:8000

Depois, rode:

```bash
cd backend
python -m uvicorn main:app --reload

A interface do usuário fica disponível em http://127.0.0.1:8000 e a documentação interativa em http://127.0.0.1:8000/docs.

Para rodar os testes automatizados da API:

```bash
pytest


Endpoints 

Método,Rota,Descrição
GET,/,Servidor web estático da interface corporativa
POST,/api/v1/enviar-email,Criptografa o conteúdo em PGP e realiza o envio via SMTPS
GET,/docs,Documentação interativa Swagger/OpenAPI

Demonstração
Interface do Usuário
![Interface](docs/interface.gif)
Recebimento do E-mail e Payload Criptografado (Ethereal Sandbox)
![E-mail](docs/email.gif)

Licença
Este projeto está sob a licença MIT — sinta-se à vontade para usar como referência de estudo.

Aviso de segurança
Este projeto usa o ambiente sandbox do Ethereal Email, sem disparo de e-mails reais para a internet. Credenciais SMTP e configurações de ambiente são carregadas via variáveis de ambiente (.env, não incluído no repositório) e nunca ficam expostas no código-fonte.