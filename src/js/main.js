import { initializeChat } from './chat.js';
import { setupEventListeners } from './eventListeners.js';

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
    setupEventListeners();
});