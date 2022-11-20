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
    # only mp4 support
}

app = Flask(__name__, template_folder='public')
app.static_folder = 'static'
app.secret_key = 'ENTER_YOUR_SECRET_KEY'
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


@app.route('/addcontent', methods=['POST', 'GET'])
def add_content():
    if request.method == 'POST':
        # database
        connection = sqlite3.connect('./database/contents.db')
        cursor = connection.cursor()

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS contents(namesurname TEXT, title TEXT, region TEXT, description TEXT, filename TEXT)')

        # datas
        namesurname = request.form.get('namesurname')
        content_title = request.form.get('contenttitle')
        region = request.form.get('region')
        description = request.form.get('description')
        filename = request.form.get('filename')

        # insert datas
        cursor.execute(
            f'INSERT INTO contents VALUES("{namesurname}","{content_title}","{region}","{description}","{filename}")')

        if True:
            connection.commit()
            connection.close()

        return '''
        Content Created<br>
        <a href="/">Back to home.</a>
        '''
    else:
        return redirect('/newcontent')


@app.route('/network')
def network():
    connection = sqlite3.connect('./database/contents.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM contents')
    datas = cursor.fetchall()

    return render_template('network.html', datas=datas)


@app.route('/network/<content>')
def view_content(content):
    connection = sqlite3.connect('./database/contents.db')
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT * FROM contents WHERE title="{content}"')
    datas = cursor.fetchall()

    return render_template('view-content.html', datas=datas)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/panel', methods=['POST'])
def view_panel():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'ENTER_ADMINISTRATOR_PASSWORD':
            return render_template('panel.html')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/addpost', methods=['POST'])
def add_post():
    connection = sqlite3.connect('./database/posts.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS posts(title TEXT, author TEXT, post TEXT)')
    
    if request.method == 'POST':
        title = request.form.get('posttitle')
        author = request.form.get('author')
        post = request.form.get('post')

        cursor.execute(
            f'INSERT INTO posts VALUES("{title}","{author}","{post}")')
        
        if True:
            connection.commit()
            connection.close()

        return '''
        Post added.
        <a href="/login">Back to panel</a>
        '''
    else:
        return redirect('/panel')


@app.route('/news')
def news():
    connection = sqlite3.connect('./database/posts.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM posts')
    datas = cursor.fetchall()

    return render_template('news.html', datas=datas)


@app.route('/news/<post>')
def post_details(post):
    connection = sqlite3.connect('./database/posts.db')
    cursor = connection.cursor()

    cursor.execute(
        f'SELECT * FROM posts WHERE title="{post}"')
    datas = cursor.fetchall()

    return render_template('post-details.html', datas=datas)


# run server
if __name__ == '__main__':
    app.run(debug=True)
