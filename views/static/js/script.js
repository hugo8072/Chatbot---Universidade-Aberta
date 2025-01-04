let currentContext = null;  // Inicialmente sem contexto selecionado
let conversationHistory = [];  // Mantém o histórico de perguntas e respostas

// Função para adicionar mensagem ao chat
function addMessage(text, className) {
    const message = document.createElement('div');
    message.textContent = text;
    message.classList.add('message', className);
    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Função para adicionar a saudação inicial e opções de temas
function addInitialMessages() {
    addMessage('Olá! Escolha o contexto que deseja utilizar:', 'bot-message');
    const themeOptions = document.createElement('div');
    themeOptions.classList.add('theme-options');
    ['Aspetos administrativos UAB', 'Modelo Pedagógico Virtual UAB', 'Temas e conteúdos de UCs 3º Ano-LEI'].forEach((theme, index) => {
        const option = document.createElement('div');
        option.textContent = theme;
        option.classList.add('theme-option');
        option.addEventListener('click', () => selectTheme(index + 1, theme));
        themeOptions.appendChild(option);
    });
    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(themeOptions);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Desabilitar o input e o botão até que um tema seja selecionado
    document.getElementById('question-input').disabled = true;
    document.getElementById('send-button').disabled = true;
}

// Função para definir o contexto com base na escolha do utilizador
function selectTheme(context, themeText) {
    currentContext = context.toString();  // Define o contexto como '1', '2', ou '3'
    const themeOptions = document.querySelector('.theme-options');
    if (themeOptions) {
        themeOptions.remove();  // Remove as opções de temas
    }
    addMessage(themeText, 'user-message');  // Mostra o tema selecionado como mensagem do utilizador
    addMessage(`Contexto ${currentContext} selecionado.`, 'bot-message');
    addMessage('Caso queira mudar de tema, escreva "mudar tema".', 'info-message');

    // Ativar o input e o botão após a seleção do tema
    document.getElementById('question-input').disabled = false;
    document.getElementById('send-button').disabled = false;
}

// Função para mostrar novamente as opções de temas
function showThemeOptions() {
    addMessage('Escolha um tema:', 'bot-message');
    const themeOptions = document.createElement('div');
    themeOptions.classList.add('theme-options');
    ['Aspetos administrativos UAB', 'Modelo Pedagógico Virtual UAB', 'Temas e conteúdos de UCs 3º Ano-LEI'].forEach((theme, index) => {
        const option = document.createElement('div');
        option.textContent = theme;
        option.classList.add('theme-option');
        option.addEventListener('click', () => selectTheme(index + 1, theme));
        themeOptions.appendChild(option);
    });
    const chatBox = document.getElementById('chat-box');
    chatBox.appendChild(themeOptions);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Desabilitar o input e o botão enquanto as opções de tema são mostradas
    document.getElementById('question-input').disabled = true;
    document.getElementById('send-button').disabled = true;
}

// Adicionar a saudação inicial e opções de temas quando a página carrega
document.addEventListener('DOMContentLoaded', addInitialMessages);

document.getElementById('send-button').addEventListener('click', function() {
    const questionInput = document.getElementById('question-input');
    const question = questionInput.value.trim();
    const chatBox = document.getElementById('chat-box');

    // Verificar se a pergunta está em branco ou apenas com espaços
    if (!question) {
        addMessage('Por favor, insira uma pergunta válida.', 'bot-message');
        questionInput.value = '';  // Limpa a caixa de entrada
        return;
    }

    // Adicionar a pergunta do utilizador ao chat
    addMessage(question, 'user-message');

    // Limpar a caixa de entrada 
    questionInput.value = '';  

    if (question.toLowerCase() === 'mudar tema') {
        showThemeOptions();
        return;  // Sai da função após mostrar as opções de temas
    }

    // Adicionar os três pontinhos indicando que o bot está a processar
    const botTypingMessage = document.createElement('div');
    botTypingMessage.classList.add('message', 'bot-message', 'typing-indicator');
    botTypingMessage.innerHTML = '<div></div><div></div><div></div>';
    chatBox.appendChild(botTypingMessage);

    // Scroll para o final do chat
    chatBox.scrollTop = chatBox.scrollHeight;

    // Enviar a pergunta para o servidor Flask com o histórico
    fetch(`http://localhost:5000/ask`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question, context: currentContext, history: conversationHistory })
    })
    .then(response => response.json())
    .then(data => {
        // Remover os três pontinhos
        chatBox.removeChild(botTypingMessage);
        
        // Adicionar a resposta do bot
        if (data.error) {
            addMessage(data.error, 'bot-message');
        } else {
            // Capitalizar a primeira letra da resposta
            const answer = data.answer.charAt(0).toUpperCase() + data.answer.slice(1);
            addMessage(answer, 'bot-message');

            // Atualizar o histórico de conversas
            conversationHistory = data.history;  // Atualiza o histórico com a resposta recebida
        }

        // Scroll para o final do chat
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);

        // Remover os três pontinhos
        chatBox.removeChild(botTypingMessage);
        
        // Adicionar a mensagem de erro do bot
        addMessage(`Erro: ${error.message}`, 'bot-message');

        // Scroll para o final do chat
        chatBox.scrollTop = chatBox.scrollHeight;
    });
});
