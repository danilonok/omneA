function openModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('back_btn').addEventListener('click', () => {


        window.electron.backButtonClick();

    });

    const deleteButtons = document.querySelectorAll('.delete-button');
    const modal = document.getElementById('modal');

    deleteButtons.forEach(button => {
        button.addEventListener('click', openModal);
    });

    

    function openModal() {
        modal.style.display = 'flex';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    const closeButton = document.querySelector('.yes-button');
    closeButton.addEventListener('click', closeModal);
    const noButton = document.querySelector('.cancel-button');
    closeButton.addEventListener('click', closeModal);
});