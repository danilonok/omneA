document.addEventListener('DOMContentLoaded', () => {
document.getElementById('history_btn').addEventListener('click', () => {
   
        window.electron.historyButtonClick();
    
});


document.getElementById('settings_btn').addEventListener('click', () => {
    
        window.electron.settingsButtonClick();
    
});

document.getElementById('send_btn').addEventListener('click', () => {
    
    window.electron.sendButtonClick();

});
});