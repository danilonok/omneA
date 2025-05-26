const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    historyButtonClick: () => ipcRenderer.send('button-clicked'),
    settingsButtonClick: () => ipcRenderer.send('settings-button-clicked'),
    sendButtonClick: () => ipcRenderer.send('send-button-clicked'),
});