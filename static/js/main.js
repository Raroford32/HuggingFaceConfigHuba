document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const serverForm = document.getElementById('server-form');
    const modelForm = document.getElementById('model-form');
    const configForm = document.getElementById('config-form');
    const serverList = document.getElementById('server-list');
    const modelList = document.getElementById('model-list');
    const serverSelect = document.getElementById('server-select');
    const modelSelect = document.getElementById('model-select');
    const tgiAddress = document.getElementById('tgi-address');
    const repairLog = document.getElementById('repair-log');
    const statusMessage = document.createElement('div');
    statusMessage.id = 'status-message';
    document.querySelector('main').appendChild(statusMessage);

    function showStatus(message, isSuccess) {
        statusMessage.textContent = message;
        statusMessage.style.color = isSuccess ? 'green' : 'red';
        setTimeout(() => {
            statusMessage.textContent = '';
        }, 3000);
    }

    function fetchServers() {
        fetch('/servers')
            .then(response => response.json())
            .then(data => {
                serverList.innerHTML = '';
                serverSelect.innerHTML = '<option value="">Select a server</option>';
                data.servers.forEach(server => {
                    const li = document.createElement('li');
                    li.textContent = `${server.name} - Command: ${server.workspace_command}`;
                    serverList.appendChild(li);

                    const option = document.createElement('option');
                    option.value = server.server_id;
                    option.textContent = server.name;
                    serverSelect.appendChild(option);
                });
            });
    }

    function fetchModels() {
        fetch('/models')
            .then(response => response.json())
            .then(data => {
                modelList.innerHTML = '';
                modelSelect.innerHTML = '<option value="">Select a model</option>';
                data.models.forEach(model => {
                    const li = document.createElement('li');
                    li.textContent = `${model.name} (${model.huggingface_id})`;
                    modelList.appendChild(li);

                    const option = document.createElement('option');
                    option.value = model.id;
                    option.textContent = model.name;
                    modelSelect.appendChild(option);
                });
            });
    }

    serverForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(serverForm);
        fetch('/servers', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                serverForm.reset();
                fetchServers();
                showStatus('Server added successfully', true);
            } else {
                showStatus('Failed to add server', false);
            }
        });
    });

    modelForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(modelForm);
        fetch('/models', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modelForm.reset();
                fetchModels();
                showStatus('Model added successfully', true);
            } else {
                showStatus('Failed to add model', false);
            }
        });
    });

    configForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const serverId = serverSelect.value;
        const modelId = modelSelect.value;

        if (!serverId || !modelId) {
            showStatus('Please select a server and a model', false);
            return;
        }

        socket.emit('configure_tgi', { server_id: serverId, model_id: modelId });
    });

    socket.on('connection_response', (data) => {
        console.log('Connected to server:', data);
    });

    socket.on('configuration_response', (data) => {
        if (data.success) {
            tgiAddress.textContent = `TGI API Address: ${data.tgi_address}`;
            showStatus('Configuration successful', true);
            displayRepairLog(data.repair_log);
        } else {
            showStatus(`Configuration failed: ${data.message}`, false);
        }
    });

    function displayRepairLog(log) {
        repairLog.innerHTML = '<h3>Repair Log:</h3>';
        log.forEach(entry => {
            const entryDiv = document.createElement('div');
            entryDiv.innerHTML = `
                <p><strong>Error:</strong> ${entry.error}</p>
                <p><strong>Suggestion:</strong> ${entry.suggestion}</p>
                <p><strong>Result:</strong> ${entry.result}</p>
                <hr>
            `;
            repairLog.appendChild(entryDiv);
        });
    }

    fetchServers();
    fetchModels();
});
