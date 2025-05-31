document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('back_btn').addEventListener('click', () => {

        window.electron.backButtonClick();

    });
});

async function fetchLogs() {
    const response = await fetch('http://127.0.0.1:8000/logs');
    if (!response.ok) {
        throw new Error('Failed to fetch logs');
    }
    return await response.json();
}

function getLogClass(type) {
    // You can customize colors/styles for each log type if you want
    switch (type) {
        case 'input_message':
            return 'log info';
        case 'current_agent':
            return 'log info';
        case 'tool_call':
            return 'log warn';
        case 'tool_result':
            return 'log warn';
        case 'agent_output':
            return 'log info';
        default:
            return 'log info';
    }
}

function renderLogs(logs) {
    const logContainer = document.getElementById('logContainer');
    logContainer.innerHTML = '';
    logs.forEach(log => {
        const tr = document.createElement('tr');
        tr.className = getLogClass(log.type);

        const tdType = document.createElement('td');
        tdType.textContent = log.type;

        const tdMsg = document.createElement('td');
        tdMsg.textContent = log.log_text;

        tr.appendChild(tdType);
        tr.appendChild(tdMsg);

        logContainer.appendChild(tr);
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const logs = await fetchLogs();
        renderLogs(logs);
    } catch (err) {
        document.getElementById('logContainer').innerHTML = '<tr><td colspan="2">Failed to load logs.</td></tr>';
        console.error(err);
    }
});
