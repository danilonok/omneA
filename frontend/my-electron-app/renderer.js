document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('history_btn').addEventListener('click', () => {
        window.electronAPI.historyButtonClick();
    });

    document.getElementById('settings_btn').addEventListener('click', () => {
        window.electronAPI.settingsButtonClick();
    });

    const sendButton = document.getElementById('send_btn');
    const inputField = document.getElementById('styled-input');

    // Set up message receiving
    window.electronAPI.onMessage((message) => {
        console.log('Received message:', message);
        // Here you can handle the received message
        // For example, display it in a chat window or process it
    });

    sendButton.addEventListener('click', () => {
        const message = inputField.value.trim();
        if (message) {
            window.electronAPI.sendMessage(message);
            inputField.value = ''; // Clear the input after sending
        }
    });

    // Also send on Enter key press
    inputField.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            const message = inputField.value.trim();
            if (message) {
                window.electronAPI.sendMessage(message);
                inputField.value = ''; // Clear the input after sending
            }
        }
    });
});