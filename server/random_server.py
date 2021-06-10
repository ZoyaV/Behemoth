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

app = Flask(__name__)
CORS(app)

hobbies = ['swim', 'art', 'IT', 'sport', 'school', 'languages', 'ecology', 'adventure']

male = 140
female = 146
age18 = 18
age18_26 = 36
age26_40 = 89
age40_60 = 9
age60 = 6

def random_timeline():
    timeline = {'time':[], 'number':[]}
    line = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0]
    N = random.randint(1, 18)
    start_point = random.randint(0, 17)
    timeline['time'] = line[start_point:start_point+N]
    for i in range(N):
        count = random.randint(1,40)
        timeline['number'].append(count)
    return timeline

def random_interests():
    global hobbies
    sets = []
    count = []
    for hobby in hobbies:
        sets.append(hobby)
        count.append(random.randint(100,200))
    happy_dict = dict(zip(sets, count))
    
    for i in range(random.randint(10, 20)):
        new_arr = np.random.permutation(hobbies)[:random.randint(2,4)].tolist()
        value_arr = [happy_dict[arg] for arg in new_arr]
        min_avalible_val = min(value_arr)
        max_avalible_val = max(value_arr)
        sets.append(new_arr)
        count.append(random.randint(min_avalible_val, max_avalible_val))
    result = []
    for i,set in enumerate(sets):
        result.append({'sets':set, 'size':count[i]})
    return result

def random_sex():
    male = random.randint(100, 200)
    female = random.randint(100, 200)
    return male, female

def random_ages():
    age18 = random.randint(100, 200)
    age18_26 = random.randint(100, 200)
    age26_40 = random.randint(100, 200)
    age40_60 = random.randint(100, 200)
    age60 = random.randint(100, 200)

    return age18,age18_26,age26_40,age40_60,age60

@app.route("/sex", methods=['GET','POST'])
def sex():
    global male, female
    # if datetime.datetime.now().minute %5 == 0:
    if request.args['complex'] == '0':
        male, female = random_sex()
    if request.args['complex'] == '1':
        male, female = random_sex()
    if request.args['complex'] == '2':
        male, female = random_sex()
    resp = make_response(jsonify({"male" : male, "female" : female}))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

_timeline = random_timeline()

@app.route("/timeline", methods=['GET','POST'])
def timeline():
    global _timeline
    # if datetime.datetime.now().minute %5 == 0:
    if request.args['complex'] == '0':
        _timeline = random_timeline()
    if request.args['complex'] == '1':
        _timeline = random_timeline()
    if request.args['complex'] == '2':
        _timeline = random_timeline()
    resp = make_response(jsonify(_timeline))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/ages", methods=['GET', 'POST'])
def ages():
    global age18, age18_26, age26_40, age40_60, age60
    # if datetime.datetime.now().minute %5 == 0:
    if request.args['complex'] == '0':
        ge18,age18_26,age26_40,age40_60,age60 = random_ages()
    if request.args['complex'] == '1':
        ge18,age18_26,age26_40,age40_60,age60 = random_ages()
    if request.args['complex'] == '2':
        ge18,age18_26,age26_40,age40_60,age60 = random_ages()
    resp = make_response(jsonify({ "age18": age18,
                     "age18_26": age18_26,
                     "age26_40": age26_40,
                     "age40_60": age40_60,
                     "age60": age60,
                     }))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

interests_chart = random_interests()
@app.route("/interests", methods=['GET','POST'])
def interests():
    global interests_chart
    # if datetime.datetime.now().minute %5 == 0:
    if request.args['complex'] == '0':
        interests_chart = random_interests()
    if request.args['complex'] == '1':
        interests_chart = random_interests()
    if request.args['complex'] == '2':
        interests_chart = random_interests()
    resp = make_response(jsonify( {'interest':interests_chart}))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


if __name__ == "__main__":
    app.run('127.0.0.1', 5000 )