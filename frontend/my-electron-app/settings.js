document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('back_btn').addEventListener('click', () => {


        window.electron.backButtonClick();

    });
    document.getElementById('logs_btn').addEventListener('click', () => {


        window.electron.logsButtonClick();

    });
    // const danger_btn = document.getElementById('danger-setting-btn');
    // const edit_btn = document.getElementById('edit-setting-btn');

    // const modal = document.getElementById('modal-text-change');
    // const dng_modal = document.getElementById('modal-danger');
    
    // edit_btn.addEventListener('click', openModal);
    // danger_btn.addEventListener('click', openDngModal);

    

    // function openModal() {
    //     modal.style.display = 'flex'; 
    // }
    // function openDngModal() {
    //     dng_modal.style.display = 'flex';
    // }
    // function closeModal() {
    //     modal.style.display = 'none'; 
    //     dng_modal.style.display = 'none';
    // }


    document.getElementById('dng_yes_btn').addEventListener('click', () => {
        closeModal();
    });
    document.getElementById('dng_cancel_btn').addEventListener('click', () => {
        closeModal();
    });
    document.getElementById('yes_btn').addEventListener('click', () => {
        closeModal();
    });
    document.getElementById('cancel_btn').addEventListener('click', () => {
        closeModal();
    });
    document.getElementById('delete_logs').addEventListener('click', async () => {
        try {
            await fetch('http://127.0.0.1:8000/logs/delete', { method: 'POST' });
            alert('Logs deleted.');
        } catch (e) {
            alert('Failed to delete logs.');
            console.error(e);
        }
    });

    document.getElementById('delete_history').addEventListener('click', async () => {
        try {
            await fetch('http://127.0.0.1:8000/history/delete', { method: 'POST' });
            alert('History deleted.');
        } catch (e) {
            alert('Failed to delete history.');
            console.error(e);
        }
    });

});