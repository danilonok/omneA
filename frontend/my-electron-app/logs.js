document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('back_btn').addEventListener('click', () => {

        window.electron.backButtonClick();

    });
});