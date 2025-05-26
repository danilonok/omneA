
document.addEventListener('DOMContentLoaded', () => {

    document.getElementsByClassName('close-button')[0].addEventListener('click', () => {

        window.electron.backButtonClick();

    });
});