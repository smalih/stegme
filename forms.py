from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

class UploadForm(FlaskForm):
    message = StringField("Message")
    operation = RadioField("Operation", choices=['Encode', 'Decode'])
    image = FileField("image", validators=[
        FileRequired(),
        FileAllowed(['png'], "PNG images only!")
    ])
    submit = SubmitField()
