export function initializeChat() {
    const chatContainer = document.getElementById('chatContainer');
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendMessage');

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleUserMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            
            // Simulate bot response
            setTimeout(() => {
                const botResponse = getBotResponse(message);
                addMessage(botResponse);
            }, 1000);
        }
    }

    function getBotResponse(message) {
        // Simple response logic - in a real application, this would be more sophisticated
        const responses = {
            hello: "Hello! How can I assist you with your health today?",
            help: "I can help you with general health questions, symptoms, and medical information. What do you need help with?",
            symptoms: "Could you please describe your symptoms in detail so I can better assist you?",
            default: "I understand your concern. While I can provide general information, please consult a healthcare professional for medical advice."
        };

        message = message.toLowerCase();
        if (message.includes('hello') || message.includes('hi')) return responses.hello;
        if (message.includes('help')) return responses.help;
        if (message.includes('symptom')) return responses.symptoms;
        return responses.default;
    }

    // Event listeners
    sendButton.addEventListener('click', handleUserMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleUserMessage();
    });
}