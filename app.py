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
import sass
import os
import time


# settings
app = Flask(__name__, template_folder='public')
app.static_folder = 'static'
app.secret_key = '1f033201deef050a886782b5'


# routes
@app.route('/')
def index():
    return render_template('home.html')


# run server
if __name__ == '__main__':
    app.run(debug = True)