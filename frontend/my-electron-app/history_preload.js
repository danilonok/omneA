const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    backButtonClick: () => ipcRenderer.send('back-button-clicked')
});

async function fetchHistory() {
    const response = await fetch('http://127.0.0.1:8000/history');
    if (!response.ok) {
        throw new Error('Failed to fetch history');
    }
    return await response.json();
}

history = fetchHistory().then(data => console.log(data)).catch(err => console.error(err));