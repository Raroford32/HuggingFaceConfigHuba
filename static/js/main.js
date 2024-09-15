document.addEventListener('DOMContentLoaded', () => {
    const socket = io({
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 20000,
    });
    const configForm = document.getElementById('config-form');
    const modelNameInput = document.getElementById('model-name');
    const connectionCommand = document.getElementById('connection-command');
    const startServerButton = document.getElementById('start-server-button');
    const serverStats = document.getElementById('server-stats');
    const tgiStats = document.getElementById('tgi-stats');

    configForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const modelName = modelNameInput.value;
        fetch('/generate_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `model_name=${encodeURIComponent(modelName)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                connectionCommand.textContent = data.command;
                startServerButton.style.display = 'block';
            } else {
                connectionCommand.textContent = `Error: ${data.message}`;
            }
        });
    });

    startServerButton.addEventListener('click', () => {
        const modelName = modelNameInput.value;
        socket.emit('start_tgi_server', { model_name: modelName });
    });

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    socket.on('server_info', (data) => {
        serverStats.innerHTML = `
            <p>CPU: ${data.cpu.toFixed(2)}%</p>
            <p>Memory: ${data.memory.toFixed(2)}%</p>
            <p>Disk: ${data.disk.toFixed(2)}%</p>
            ${data.gpu_util !== null ? `<p>GPU Utilization: ${data.gpu_util.toFixed(2)}%</p>` : ''}
            ${data.gpu_memory !== null ? `<p>GPU Memory: ${data.gpu_memory.toFixed(2)}%</p>` : ''}
        `;
    });

    socket.on('tgi_server_response', (data) => {
        if (data.success) {
            tgiStats.innerHTML = `<p>${data.message}</p>`;
        } else {
            tgiStats.innerHTML = `<p>Error: ${data.message}</p>`;
        }
    });
});
