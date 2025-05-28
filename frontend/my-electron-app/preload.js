const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    sendMessage: (message) => {
        ipcRenderer.send('send-message', message);
    },
    onMessage: (callback) => {
        ipcRenderer.on('websocket-message', (event, message) => callback(message));
    },
    historyButtonClick: () => ipcRenderer.send('button-clicked'),
    exitAppButtonClick: () => ipcRenderer.send('exit-app-button-clicked'),
    settingsButtonClick: () => ipcRenderer.send('settings-button-clicked'),
    sendButtonClick: () => ipcRenderer.send('send-button-clicked'),
});