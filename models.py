from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    server_id = db.Column(db.String(36), nullable=False, unique=True)
    workspace_command = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'server_id': self.server_id,
            'workspace_command': self.workspace_command
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
