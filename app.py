import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from forms import UploadForm
import requests
from PIL import Image
import time

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
# print("API Key: ", os.getenv('API_KEY'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#             encode(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)), "hello, this is a test message", os.path.join(HIDDEN_FOLDER, filename))

#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''



category = 'nature'
categories='nature, city, technology, food, still_life, abstract, wildlife'.split(", ")


def get_random_image_from_api(category='nature'):
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
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
                encode(image, message, app.config['ENCODE_FOLDER'] + filename)
                flash('Message successfully encoded', 'success')
                return redirect(url_for('download', name=filename))
            elif operation == 'Decode':
                hidden_message = decode(form.image.data)
                print("decode output: ", hidden_message)
                return "<h1>" + hidden_message + "<h1>"

            return redirect(url_for('upload'))
    return render_template('index.html', form=form)
    #         if 'file' not in request.files:
    #             flash('No file part')
    #             return redirect(request.url)
    #         file = request.files['file']
    #         # If the user does not select a file, the browser submits an
    #         # empty file without a filename.
    #         if file.filename == '':
    #             flash('No selected file')
    #             return redirect(request.url)
    #         if file and allowed_file(file.filename):
    #             filename = secure_filename(file.filename)
    #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #             encode(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)), "hello, this is a test message", os.path.join(HIDDEN_FOLDER, filename))

    #             return redirect(url_for('download_file', name=filename))

    # return render_template('upload.html', form=form)


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



@app.route('/hidden/<name>')
def download(name):
    return send_from_directory(app.config['ENCODE_FOLDER'], name)

