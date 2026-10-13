document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('formularioEmailSeguro');
    const botaoEnviar = document.getElementById('botaoEnviar');
    const caixaAlerta = document.getElementById('caixaAlerta');

    const exibirAlerta = (mensagem, ehSucesso) => {
        caixaAlerta.className = `alerta ${ehSucesso ? 'alerta-sucesso' : 'alerta-erro'}`;
        caixaAlerta.textContent = mensagem;
        caixaAlerta.style.display = 'block';
    };

    formulario.addEventListener('submit', async (evento) => {
        evento.preventDefault();
        caixaAlerta.style.display = 'none';

        const dados = {
            email_destino: document.getElementById('emailDestino').value.trim(),
            assunto: document.getElementById('assunto').value.trim(),
            conteudo: document.getElementById('conteudo').value.trim()
        };

        if (!dados.email_destino || !dados.assunto || !dados.conteudo) {
            exibirAlerta('Erro [400]: Por favor, preencha todos os campos.', false);
            return;
        }

        botaoEnviar.disabled = true;
        botaoEnviar.textContent = 'Enviando...';

        try {
            const resposta = await fetch('/api/v1/enviar-email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });

            const resultado = await resposta.json();

            if (resposta.ok) {
                exibirAlerta('Mensagem enviada com sucesso.', true);
                formulario.reset();
            } else {
                // Captura o código de status HTTP (ex: 422, 500, 502) e o detalhe técnico enviado pelo Back-end
                const detalheErro = resultado.detail 
                    ? (typeof resultado.detail === 'string' ? resultado.detail : JSON.stringify(resultado.detail))
                    : 'Falha no processamento.';
                
                exibirAlerta(`Erro [HTTP ${resposta.status}]: ${detalheErro}`, false);
            }
        } catch (erro) {
            exibirAlerta('Erro de Conexão: Não foi possível alcançar o servidor.', false);
        } finally {
            botaoEnviar.disabled = false;
            botaoEnviar.textContent = 'Enviar Mensagem';
        }
    });
});