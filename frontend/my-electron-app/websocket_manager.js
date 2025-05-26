const WebSocket = require('ws');
const { BrowserWindow, ipcMain } = require('electron');

let socket = null;

function connectToWebSocket() {
    try {
        socket = new WebSocket("ws://localhost:8000/ws/agent");

        socket.onopen = () => {
            console.log("Connected to WebSocket server");
        };

        socket.onmessage = (event) => {
            console.log('WebSocket received message:', event.data);
            // Send the received message to the main process
            ipcMain.emit('websocket-message', null, event.data);
        };

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed");
        };

        return socket;
    } catch (error) {
        console.error("Failed to connect to WebSocket:", error);
        return null;
    }
}

module.exports = {
    connectToWebSocket,
    getSocket: () => socket
};