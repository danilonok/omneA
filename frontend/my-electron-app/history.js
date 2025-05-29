document.addEventListener('DOMContentLoaded', async () => {

    const entriesDiv = document.querySelector('.entries');
    entriesDiv.innerHTML = ''; // Clear static entries

    try {
        const history = await fetchHistory();
        history.forEach(entry => {
            entriesDiv.appendChild(createHistoryEntry(entry));
        });
    } catch (err) {
        entriesDiv.innerHTML = '<div>Error loading history.</div>';
        console.error(err);
    }
});


async function fetchHistory() {
    const response = await fetch('http://127.0.0.1:8000/history');
    if (!response.ok) {
        throw new Error('Failed to fetch history');
    }
    return await response.json();
}

function createHistoryEntry(entry) {
    const div = document.createElement('div');
    div.className = 'history-entry';

    const span = document.createElement('span');
    span.textContent = entry.title + ' (' + new Date(entry.timestamp).toLocaleString() + ')';

    const iconsDiv = document.createElement('div');
    iconsDiv.className = 'icons';

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'button';
    deleteBtn.innerHTML = '<img src="img/delete-dustbin-01.svg">';
    // Add delete logic here if needed

    const refreshBtn = document.createElement('button');
    refreshBtn.className = 'button';
    refreshBtn.innerHTML = '<img src="img/Refresh cw.svg">';
    // Add refresh logic here if needed

    iconsDiv.appendChild(deleteBtn);
    iconsDiv.appendChild(refreshBtn);

    div.appendChild(span);
    div.appendChild(iconsDiv);

    return div;
}
