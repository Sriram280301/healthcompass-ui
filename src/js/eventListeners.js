export function setupEventListeners() {
    const startChatButton = document.getElementById('startChat');
    const closeButton = document.getElementById('closeChat');
    const chatContainer = document.getElementById('chatContainer');

    startChatButton.addEventListener('click', () => {
        chatContainer.classList.remove('hidden');
    });

    closeButton.addEventListener('click', () => {
        chatContainer.classList.add('hidden');
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}