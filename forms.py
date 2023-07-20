from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

class UploadForm(FlaskForm):
    message = StringField("Message", [validators.InputRequired()])
    image = FileField("image", validators=[
        FileRequired(),
        FileAllowed(['png'], "PNG images only!")
    ])
    submit = SubmitField("Hide")
