document.addEventListener('DOMContentLoaded', () => {
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

    const closeButton = document.querySelector('.close-button');
    closeButton.addEventListener('click', closeModal);
});