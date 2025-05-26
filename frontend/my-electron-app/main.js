const { app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');


let win = null
let stepWindows = [];
const stepHeight = 172; 
const baseX = 100;
const baseY = 600;
const mainWindowHeight = 220;
const mainWindowWidth = 700;



let stepCount = 0;
let stepInterval = null;
let currentWindow = null;


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

  win.loadFile('info_modal.html'); 
  console.log('loaded history')
}

function loadSettingsWindow(){

  if (win) {
    win.close();
    console.log('closed main')
  }
  win = new BrowserWindow({
      width: mainWindowWidth,
      height: 390,
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
      height: 376,
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

app.whenReady().then(() => {
  loadMainWindow()
})

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





ipcMain.on('send-button-clicked', (event) => {
    
  stepInterval = setInterval(() => {
        step_num = stepCount + 1
        
        createStepWindow(step_num);
    }, 500);
})


function createStepWindow(title) {
  
  if(stepCount > 1){
    clearInterval(stepInterval)
  }
  stepCount++;
  stepWindows.slice().reverse().forEach((win, index) => {
      win.setBounds({
          x: baseX,
          y: baseY + stepHeight * 2 - (index + 1) * stepHeight - (index + 2)*10,
          width: mainWindowWidth,
          height: stepHeight,
      });
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
    document.getElementById('step-number').innerText = ${title};
`);

  stepWindows.push(stepWindow);
}