import os
os.environ['KERAS_BACKEND'] = 'theano'
import librosa
import numpy as np
from keras.models import model_from_json
import keras
import tensorflow as tf
import pandas as pd
import soundfile as sf
from flask import Flask, flash, request, redirect, url_for
from keras import backend as K 
import json

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")

opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)

loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

app = Flask(__name__)

def predict_speech_emotion(filename):
	f = sf.SoundFile(filename)

	duration = int(len(f) / f.samplerate)

	X, sample_rate = librosa.load(filename, res_type='kaiser_fast',duration=duration,sr=22050*2,offset=0.5)
	sample_rate = np.array(sample_rate)

	list_mfccs = []
	for i in range(X.shape[0]//110250):
		low = 110250*i
		high = 110250*i+110250
		mfccs = np.mean(librosa.feature.mfcc(y=X[low:high], sr=sample_rate, n_mfcc=13),axis=0)
		list_mfccs.append(mfccs)

	livedf2= pd.DataFrame(data=list_mfccs)

	twodim= np.expand_dims(livedf2, axis=2)

	livepreds = loaded_model.predict(twodim, batch_size=32,verbose=1)

	livepreds1=livepreds.argmax(axis=1)

	male_calm={
			1:'female_sad',
			2:'female_fearful',
			3:'male_fearful',
			4:'female_fearful',
			5:'female_happy',
			6:'male_calm',
			7:'male_angry',
			8:'female_angry',
			9:'female_happy'
			}


	list_predicted = []
	for i in livepreds1:
		list_predicted.append(male_calm[i])

	diction = {}
	for (i, value) in enumerate(list_predicted):
		diction[str(i)] = str(value).split('_')[1]

	js = json.dumps(diction)

	return js

@app.route('/')
def index():
    return "Hello ,World!"

@app.route('/speechemotion', methods = ['GET','POST'])
def check_speech():
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
                return predict_speech_emotion('temp/'+str(file.filename))
        else:
            print('Not found')
            return "Bhai nahi ayi"
