const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    backButtonClick: () => ipcRenderer.send('back-button-clicked'),
});