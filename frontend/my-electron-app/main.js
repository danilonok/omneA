const { app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const { connectToWebSocket, getSocket } = require('./websocket_manager');

let win = null
let stepWindows = [];
const stepHeight = 200; 
const baseX = 100;
const baseY = 0;
const mainWindowHeight = 220;
const mainWindowWidth = 700;



let stepCount = 0;
let stepInterval = null;
let currentWindow = null;


function closeApp(){
    app.quit();
}

function loadMainWindow () {
  if (win) {
    win.close();
    console.log('closed settings/history')

  }
  win = new BrowserWindow({
    height: mainWindowHeight,
    width: mainWindowWidth,
    x: baseX,
    y: baseY + stepHeight * 3, 
    resizable: true,
    frame: false,
    transparent: true,
    webPreferences: {
      nodeIntegration: false,  
      contextIsolation: true,  
      preload: path.join(__dirname, 'preload.js') 
  }
  
  })

  win.loadFile('main.html')
  console.log('loaded main')
  currentWindow = win

}

function loadHistoryWindow(){
  
  if (win) {
    win.close();
    console.log('closed main')
  }

  win = new BrowserWindow({
      width: mainWindowWidth,
      height: 450,
      frame: false,
      x: baseX,
      y: baseY + stepHeight * 3 + mainWindowHeight - 450,
      transparent: true,
      webPreferences: {
          nodeIntegration: true,
          // preloads are quite the same
          preload: path.join(__dirname, 'history_preload.js')
      }
  });

  win.loadFile('history.html'); 
  console.log('loaded history')
}

function loadInfoModalWindow(content, time){
  if (win) {
    win.close();
    console.log('closed main')
  }
  // Close step windows safely
  stepWindows.forEach((win, index) => {
    if (win && !win.isDestroyed()) {
      win.close();
    }
  });
  // Optionally clear the array if you want to remove references
  stepWindows = [];

  win = new BrowserWindow({
      width: mainWindowWidth,
      height: 600,
      frame: false,
      x: baseX,
      y: baseY + stepHeight * 3 + mainWindowHeight - 600,
      transparent: true,
      webPreferences: {
          nodeIntegration: true,
          // preloads are quite the same
          preload: path.join(__dirname, 'history_preload.js')
      }
  });

  win.loadFile('info_modal.html'); 
  win.webContents.executeJavaScript(`
    document.getElementById('content').innerText = ${JSON.stringify(content)};
    document.getElementById('time').innerText = ${JSON.stringify(time)};

  `);
  console.log('loaded history')
}

function loadSettingsWindow(){

  if (win) {
    win.close();
    console.log('closed main')
  }
  win = new BrowserWindow({
      width: mainWindowWidth,
      height: 314,
      frame: false,
      x: baseX,
      y: baseY + stepHeight * 3 + mainWindowHeight - 390,
      webPreferences: {
          nodeIntegration: true,
          preload: path.join(__dirname, 'settings_preload.js') 
      }
  });

  win.loadFile('settings.html'); 
  console.log('loaded settings')
}

function loadLogsWindow(){

  if (win) {
    win.close();
    console.log('closed settings')
  }

  win = new BrowserWindow({
      width: mainWindowWidth,
      height: 449,
      frame: false,
      x: baseX,
      y: baseY + stepHeight * 3 + mainWindowHeight - 376,
      webPreferences: {
          nodeIntegration: true,
          preload: path.join(__dirname, 'logs_preload.js') 
      }
  });

  win.loadFile('logs.html'); 
  console.log('loaded logs')

}

// event listeners

app.whenReady().then(async () => {
    try {
        loadMainWindow();
        await connectToWebSocket();
    } catch (error) {
        console.error('Failed to initialize:', error);
    }
});

ipcMain.on('button-clicked', (event) => {
  loadHistoryWindow()
})

ipcMain.on('settings-button-clicked', (event) => {
  loadSettingsWindow()
})


ipcMain.on('logs-button-clicked', (event) => {
  loadLogsWindow()
})


ipcMain.on('back-button-clicked', (event) => {
  loadMainWindow()
})
ipcMain.on('exit-app-button-clicked', (event) => {
  closeApp()
})







ipcMain.on('send-message', (event, message) => {
    const socket = getSocket();
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        console.error('WebSocket is not connected');
    }
});

ipcMain.on('websocket-message', (event, message) => {

  let parsed;
  try {
    parsed = JSON.parse(message);
  } catch (e) {
    console.error('Invalid JSON message received:', message);
    return;
  }
  console.log('Received WebSocket message in main:', message);

  // if message is report, show in in info modal
  if(parsed['type'] === 'report'){

    loadInfoModalWindow(parsed['content'], parsed['time']);
  }
  else{
    console.log('test')
    createStepWindow(parsed['content'], parsed['reason']);
  }
  
  
});

function createStepWindow(title, reason) {
  if(stepCount > 1){
    clearInterval(stepInterval)
  }
  stepCount++;
  // Filter out destroyed windows before updating positions
  stepWindows = stepWindows.filter(win => !win.isDestroyed());
  stepWindows.slice().reverse().forEach((win, index) => {
      if (!win.isDestroyed()) {
        win.setBounds({
            x: baseX,
            y: baseY + stepHeight * 2 - (index + 1) * stepHeight - (index + 2)*10,
            width: mainWindowWidth,
            height: stepHeight,
        });
      }
  });

  let stepWindow = new BrowserWindow({
      frame: false,
      width: mainWindowWidth,
      height: stepHeight,
      x: baseX,
      y: baseY + stepHeight * 2 - 10,
      alwaysOnTop: true,
      webPreferences: {
          nodeIntegration: true,
      },
  });

  stepWindow.loadFile('step.html');
  stepWindow.webContents.executeJavaScript(`
    document.getElementById('header_text').innerText = ${JSON.stringify(title)};
    document.getElementById('reason_text').innerText = ${JSON.stringify(reason)};
  `);

  stepWindows.push(stepWindow);
}