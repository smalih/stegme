from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, RadioField, validators
from wtforms.validators import Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename



class UploadForm(FlaskForm):
    message = StringField("Message")
    # image = FileField("image", validators=[
    #     FileAllowed(['png'], "PNG images only!")
    # ])
    submit = SubmitField()

class RegisterForm(FlaskForm):
    fname = StringField("Firstname", [validators.InputRequired()])
    surname = StringField("Surname", [validators.InputRequired()])
    email = EmailField("Email", [validators.InputRequired("Please enter your email address"), Email()])
    password = PasswordField(validators=[validators.Length(min=8, message='Password must be at least 8 characters in length')])
    confirm = PasswordField(validators=[validators.EqualTo('password', 'Password mismatch')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", [validators.InputRequired("Please enter your email address")])
    password = PasswordField(validators=[validators.Length(min=8, message='Password must be at least 8 characters in length')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("Log in")

