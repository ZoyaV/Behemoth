import io
import random
from typing import Optional, List
import numpy as np
import datetime
import time

from flask import Flask, request, jsonify, request, make_response
from flask_cors import CORS

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

import json

app = Flask(__name__)
CORS(app)

@app.route("/interests", methods=['GET','POST'])
def interests():
    with open("../json/interests_chart.json", "r") as read_file:
        interests_chart = json.load(read_file)
    resp = make_response(jsonify( interests_chart))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@app.route("/ages", methods=['GET', 'POST'])
def ages():
    with open("../json/human_description.json", "r") as read_file:
        ages = json.load(read_file)
    ages.pop('male')
    ages.pop('female')
    resp = make_response(jsonify(ages))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


@app.route("/sex", methods=['GET','POST'])
def sex():
    with open("../json/human_description.json", "r") as read_file:
        sex = json.load(read_file)
    sex.pop('age18')
    sex.pop('age18_26')
    sex.pop('age26_40')
    sex.pop('age40_60')
    sex.pop('age60')
    resp = make_response(jsonify(sex))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

@app.route("/timeline", methods=['GET','POST'])
def timeline():
    with open("../json/camera_data.json", "r") as read_file:
        _timeline = json.load(read_file)
    print(_timeline)
    resp = make_response(jsonify(_timeline))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

if __name__ == "__main__":
    app.run('127.0.0.1', 5000 )