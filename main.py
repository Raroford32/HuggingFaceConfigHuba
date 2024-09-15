from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from config import Config
from utils import generate_workspace_command
import subprocess

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=20, ping_interval=15)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_command', methods=['POST'])
def generate_command():
    model_name = request.form.get('model_name')
    if not model_name:
        return jsonify({'success': False, 'message': 'Model name is required'})
    
    connection_command = generate_workspace_command(model_name)
    return jsonify({'success': True, 'command': connection_command})

@socketio.on('connect')
def handle_connect():
    emit('connection_response', {'data': 'Connected'})

@socketio.on('start_tgi_server')
def handle_start_tgi_server(data):
    model_name = data.get('model_name')
    if not model_name:
        emit('tgi_server_response', {'success': False, 'message': 'Model name is required'})
        return

    command = generate_workspace_command(model_name)
    try:
        # Start the TGI server process
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        emit('tgi_server_response', {'success': True, 'message': 'TGI server starting'})
    except Exception as e:
        emit('tgi_server_response', {'success': False, 'message': f'Failed to start TGI server: {str(e)}'})

@socketio.on('server_info')
def handle_server_info(data):
    emit('server_info', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
