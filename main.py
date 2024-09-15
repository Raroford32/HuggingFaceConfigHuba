from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from config import Config
from models import db, Server, Model
from forms import ServerForm, ModelForm
from utils import generate_workspace_command, configure_tgi

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
socketio = SocketIO(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servers', methods=['GET', 'POST'])
def servers():
    form = ServerForm()
    if form.validate_on_submit():
        server_id, workspace_command = generate_workspace_command()
        server = Server(
            name=form.name.data,
            server_id=server_id,
            workspace_command=workspace_command
        )
        db.session.add(server)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Server added successfully', 'server': server.to_dict()})
    
    servers = Server.query.all()
    return jsonify({'servers': [server.to_dict() for server in servers]})

@app.route('/models', methods=['GET', 'POST'])
def models():
    form = ModelForm()
    if form.validate_on_submit():
        model = Model(
            name=form.name.data,
            huggingface_id=form.huggingface_id.data
        )
        db.session.add(model)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Model added successfully'})
    
    models = Model.query.all()
    return jsonify({'models': [model.to_dict() for model in models]})

@socketio.on('connect')
def handle_connect():
    emit('connection_response', {'data': 'Connected'})

@socketio.on('configure_tgi')
def handle_configure_tgi(data):
    server_id = data['server_id']
    model_id = data['model_id']
    
    server = Server.query.filter_by(server_id=server_id).first()
    model = Model.query.get(model_id)
    
    if not server or not model:
        emit('configuration_response', {'success': False, 'message': 'Invalid server or model'})
        return
    
    try:
        tgi_address, repair_log = configure_tgi(request.sid, model)
        emit('configuration_response', {'success': True, 'tgi_address': tgi_address, 'repair_log': repair_log})
    except Exception as e:
        emit('configuration_response', {'success': False, 'message': f'Configuration failed: {str(e)}'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
