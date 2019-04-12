from flask import Flask, flash, request, redirect, url_for
from vggish_inference_demo import OutEmbeddings
import os
import pandas as pd
import numpy as np
from keras.models import model_from_json
import matplotlib.pyplot as plt
from statistics import mean
import json
import soundfile as sf
from keras import backend as K


def return_confidence(filename):
    json_file = open('model/confidence_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model/confidence_model.h5")

    Oeg = OutEmbeddings()

    x = Oeg.run('temp/'+str(filename))
    div = 1
    xx = []
    for i in range((len(x)//div)):
        xx.append(list(np.mean(x[i:i+div], axis = 0)))
    xx = np.array(xx).reshape(-1,1,128)
    out = np.array(loaded_model.predict(np.array(xx)))

    y = []
    for i in range(out.shape[0]):
        y.append(np.argmax(out[i]))
    y = np.repeat(np.array(y),div)
    diction = {}
    for (i,value) in enumerate(y):
        diction[str(i)] = str(value)
    js = json.dumps(diction)

    K.clear_session()

    return js

    
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello ,World!"

@app.route('/confidence', methods = ['GET','POST'])
def check_confidence():
    if request.method == 'GET':
        print('chal gya')
        return "helo"

    if request.method == 'POST':
        if request.files: 
            file = request.files['wavFile']
            if file.filename == '':
                print('Not filename')
                return "filename not exist"
            else:
                file.save('./temp/' + file.filename)
                print('done')
                return return_confidence(file.filename)
        else:
            print('Not found')
            return "Bhai nahi ayi"