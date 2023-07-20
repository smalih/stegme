from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

class UploadForm(FlaskForm):
    message = StringField("Message")
    file = FileField("File")
    submit = SubmitField("Hide")


