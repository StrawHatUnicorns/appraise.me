# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from bookshelf import get_model
from flask import Flask, Blueprint, redirect, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
crud = Blueprint('crud', __name__)

# [START list]
@crud.route("/")
def index():
    return render_template("app_body.html", title = "Home")

@crud.route('/', methods = ['GET','POST'])
def upload():
    target = os.path.join(APP_ROOT,'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "./".join([target,filename])
        print(destination)
        file.save(destination)
    return render_template("app_body.html", title = "Home")
