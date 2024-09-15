from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ServerForm(FlaskForm):
    name = StringField('Server Name', validators=[DataRequired()])
    hostname = StringField('Hostname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])

class ModelForm(FlaskForm):
    name = StringField('Model Name', validators=[DataRequired()])
    huggingface_id = StringField('Hugging Face Model ID', validators=[DataRequired()])
