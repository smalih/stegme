import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, send_file, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import UploadForm, RegisterForm, LoginForm
import requests
import time
import random
import bcrypt

# from steg import Encode, Decode
from steg_lsb import encode, decode

from db_schema import db, User


UPLOAD_FOLDER = './uploads/'
ENCODE_FOLDER = './encoded/'
DECODE_FOLDER = './decode/'
HIDDEN_FOLDER = './hidden/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///main.sqlite'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HIDDEN_FOLDER'] = HIDDEN_FOLDER
app.config['ENCODE_FOLDER'] = ENCODE_FOLDER
app.config['DECODE_FOLDER'] = DECODE_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    # dbinit()
    db.drop_all()
    db.create_all()


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

category = 'nature'
categories='nature, city, technology, food, still_life, abstract, wildlife'.split(", ")


def get_random_image_from_api():
    api_url = f'https://api.api-ninjas.com/v1/randomimage?category={random.choice(categories)}'
    response = requests.get(api_url, headers={'X-Api-Key': 'vUkWtBsXjrU12mz7Ep8YdQ==TYN8vUz4sZ34Rfe2', 'Accept': 'image/png'}, stream=True)
    if response.status_code == requests.codes.ok:
        return response.raw
    raise ValueError("Error - status code NOT OK")

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        # if form.validate_on_submit():
        if True:
            message = request.form['message']
            operation = request.form['operation']
            image = request.files.get('image')

            print("image type:", type(image))
 
            if operation == 'Encode':
                if not(message):
                    flash("Message field cannot be left blank")
                    return redirect(url_for('upload'))
                if not(image) :
                    print("No image supplied, getting random one from API")
                    image = get_random_image_from_api()
            
                # form.image.data.save(app.config['UPLOAD_FOLDER'] + filename)
                filename = time.strftime("%d_%m_%Y-%H_%M_%S") + ".png"
                enc_image = encode(image, message, app.config['ENCODE_FOLDER'] + filename)
                # enc_image2 = encode(image, message)

                # return send_file(enc_image, as_attachment=True, download_name=filename)
                flash('Message successfully encoded', 'success')
                print("encoded")
                # session['encoded_file'] = enc_image2
                # session['encoded_filename'] = filename
                print("after storing in session var")
                return render_template('encoded.html', filename=filename)
            elif operation == 'Decode':
                hidden_message = decode(image)
                print("decode output: ", hidden_message)
                session['hidden_message'] = hidden_message
                return redirect(url_for('decoded'))

            return redirect(url_for('upload'))
    return render_template('index.html', form=form)



@app.route('/decoded', methods=['GET'])
def decoded():
    hidden_message = session.get('hidden_message')
    return render_template('decoded.html', hidden_message=hidden_message)

@app.route('/genfile', methods=['GET'])
def gen_file():

    category = 'nature'
    categories='nature, city, technology, food, still_life, abstract, wildlife'.split(", ")
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'vUkWtBsXjrU12mz7Ep8YdQ==TYN8vUz4sZ34Rfe2', 'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        with open('img.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print("Error:", response.status_code, response.text)
    return redirect(url_for('upload_file'))

@app.route('/download/<name>', methods=["POST"])
def download(name):
    print("in download")
    # return send_from_directory(app.config['ENCODE_FOLDER'], name, as_attachment=True)
    return send_file(app.config['ENCODE_FOLDER']+ name, as_attachment=True)
    # return render_template('encoded.html', file=session['encoded_file'], name=name)


@app.route('/index')
def index():
    return redirect(url_for('upload'))

# user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            fname = request.form['fname']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']
            confirm = request.form['confirm']
            
            if User.query.filter_by(email=email).first():
                flash('Email address already registered. Please try again with a different email address or log in', category='error')
            elif (password != confirm) :
                flash('Passwords do not match', category='error')
            
            else:
                hashed = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())  
                new_user = User(email, hashed)
                new_user.fname = fname
                new_user.surname = surname
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                new_user = User.query.filter_by(email=email).first() # is this line needed?
                flash('You have successfully registered', 'success')
                return redirect(url_for('upload'))
        else:
            flash('Register form not valid', category='error')
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. Please log out to log in with a different account', 'warning')
        return redirect(url_for('upload'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user:
                registered_hash = user.password_hash
                if bcrypt.checkpw(password.encode(), registered_hash):
                    flash(f'You have been logged in', category='success')
                    remember = True if request.form.get('remember_me') else False
                    login_user(user, remember=remember)
                    print(request.args.get('next'))
                    return redirect(url_for(request.args.get('next', default='index', type = str)))
                else:
                    flash('Incorrect password. Please check your email and password match and try again.', category='error')
            else:
                flash('Email address not recognised. Please try again.', category='error')
    return render_template('login.html', form=form)


def dbinit():
    passwd = 'adminadmin'
    hashed = bcrypt.hashpw(passwd.encode(), salt=bcrypt.gensalt())
    admin_user = User('admin@admin.com', hashed)
    admin_user.fname = 'Admin'
    admin_user.surname = 'User'
    db.session.add(admin_user)
    db.session.commit()


with app.app_context():
    dbinit()

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        flash('You have been logged out', category='success')
        logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")