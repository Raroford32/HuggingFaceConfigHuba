from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    workspace_command = db.Column(db.String(200), nullable=False)
    connected = db.Column(db.Boolean, default=False)
    server_info = db.Column(db.JSON)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'workspace_command': self.workspace_command,
            'connected': self.connected,
            'server_info': self.server_info
        }

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    huggingface_id = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'huggingface_id': self.huggingface_id
        }
