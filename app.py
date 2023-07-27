import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from forms import UploadForm
import requests
import time
import random


# from steg import Encode, Decode
from steg_lsb import encode, decode


UPLOAD_FOLDER = './uploads/'
ENCODE_FOLDER = './encoded/'
DECODE_FOLDER = './decode/'
HIDDEN_FOLDER = './hidden/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HIDDEN_FOLDER'] = HIDDEN_FOLDER
app.config['ENCODE_FOLDER'] = ENCODE_FOLDER
app.config['DECODE_FOLDER'] = DECODE_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
        if form.validate_on_submit():
            message = request.form['message']
            operation = request.form['operation']
            
            if operation == 'Encode':
                if not(message):
                    flash("Message field cannot be left blank")
                    return redirect(url_for('upload'))
                if not(form.image.data) :
                    print("No image supplied, getting random one from API")
                    image = get_random_image_from_api()
                else:
                    image = form.image.data
            
                # form.image.data.save(app.config['UPLOAD_FOLDER'] + filename)
                filename = time.strftime("%d_%m_%Y-%H_%M_%S") + ".png"
                enc_image = encode(image, message, app.config['ENCODE_FOLDER'] + filename)
                # return send_file(enc_image, as_attachment=True, download_name=filename)
                flash('Message successfully encoded', 'success')
                return redirect(url_for('download', name=filename))
            elif operation == 'Decode':
                hidden_message = decode(form.image.data)
                print("decode output: ", hidden_message)
                return "<h1>" + hidden_message + "<h1>"

            return redirect(url_for('upload'))
    return render_template('index.html', form=form)

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/encoded/<name>')
def download(name):
    return send_from_directory(app.config['ENCODE_FOLDER'], name, as_attachment=True)

