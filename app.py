# created by ekin varli
# coding: utf-8


"""
e-Math Project
--------------


Author: Ekin VARLI <ekinnos@tutanota.com>
Core Language: Python
Libraries: Flask, SQLite, Sass, Markdown...
Setup Command: pip install -r requirements.txt (if your system is linux, do pip3 install...)


MIT License

Copyright (c) 2022 Ekin VARLI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


# flask core
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash

from werkzeug.utils import secure_filename


# additional modules
import sqlite3
import markdown
import os
import time


# settings
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {
    'mp4',
    'ogg',
    'png',
    'jpg',
    'jpeg',
    'gif'
}

app = Flask(__name__, template_folder='public')
app.static_folder = 'static'
app.secret_key = '1f033201deef050a886782b5'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# routes
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/newcontent', methods=['GET', 'POST'])
def new_content():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    namesurname = request.args.get('namesurname')
    content_title = request.args.get('title')
    region = request.args.get('region')
    return render_template('newcontent.html', namesurname=namesurname, title=content_title, region=region)
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''


@app.route('/addcontent', methods=['POST', 'GET'])
def add_content():
    # database
    connection = sqlite3.connect('./database/contents.db')
    cursor = connection.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS contents(namesurname TEXT, title TEXT, region TEXT, description TEXT, filename TEXT)')


    # datas
    namesurname = request.args.get('namesurname')
    content_title = request.args.get('title')
    region = request.args.get('region')
    description = request.args.get('description')
    filename = request.args.get('file')


    # insert datas
    cursor.execute(
        f'INSERT INTO contents VALUES("{namesurname}","{content_title}","{region}","{description}","{filename}")')

    if True:
        connection.commit()
        connection.close()

    return 'Content added.'


# run server
if __name__ == '__main__':
    app.run(debug=True)
