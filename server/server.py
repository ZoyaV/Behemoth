import io
import random
from typing import Optional, List
import numpy as np
import datetime

from flask import Flask, request, jsonify, request

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

hobbies = ['swim', 'art', 'IT', 'sport', 'school', 'languages', 'ecology', 'adventure']

male = 140
female = 146
age18 = 18
age18_26 = 0
age26_40 = 89
age40_60 = 9
age60 = 6


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
    if datetime.datetime.now().minute %5 == 0:
        if request.args['complex'] == '0':
            male, female = random_sex()
        if request.args['complex'] == '1':
            male, female = random_sex()
        if request.args['complex'] == '2':
            male, female = random_sex()

    return jsonify({ "male": male,  "female": female})


@app.route("/ages", methods=['GET', 'POST'])
def ages():
    global age18, age18_26, age26_40, age40_60, age60
    if datetime.datetime.now().minute %5 == 0:
        if request.args['complex'] == '0':
            ge18,age18_26,age26_40,age40_60,age60 = random_ages()
        if request.args['complex'] == '1':
            ge18,age18_26,age26_40,age40_60,age60 = random_ages()
        if request.args['complex'] == '2':
            ge18,age18_26,age26_40,age40_60,age60 = random_ages()
    return jsonify({ "age18": age18,
                     "age18_26": age18_26,
                     "age26_40": age26_40,
                     "age40_60": age40_60,
                     "age60": age60,
                     })

interests_chart = random_interests()
@app.route("/interests", methods=['GET','POST'])
def interests():
    global interests_chart
    if datetime.datetime.now().minute %5 == 0:
        if request.args['complex'] == '0':
            interests_chart = random_interests()
        if request.args['complex'] == '1':
            interests_chart = random_interests()
        if request.args['complex'] == '2':
            interests_chart = random_interests()
    return jsonify( {'interst':interests_chart})


if __name__ == "__main__":
    app.run('127.0.0.1', 5000 )