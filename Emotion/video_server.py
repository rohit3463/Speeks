import os
os.environ['KERAS_BACKEND'] = 'theano'
import cv2
import numpy as np
from keras.models import load_model
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
import dlib
from flask import Flask, flash, request, redirect, url_for
import json
from keras import backend as K


# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0
# set_session(tf.Session(config=config))

detector = dlib.get_frontal_face_detector()
model = load_model('model_5-49-0.62.hdf5')
model.get_config()

target = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

def predict_face_expression(filename = 'temp/yep.mp4'):
	print("in the function")
	cap = cv2.VideoCapture(filename)

	targets = []
	i = 0
	while cap.isOpened():
		ret, frame = cap.read()
		# print(frame)
		if ret == True:
			(h_frame, w_frame) = frame.shape[:2]
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			faces = detector(gray, 1)

			for face in faces:
				(x1, y1, x2, y2) = (face.left(), face.top(), face.right(), face.bottom())
				x = int(x1)
				y = int(y1)
				w = int(x2 - x1)
				h = int(y2 - y1)
				x = int(x - 0.1*w) if int(x - 0.1*w)>0 else 0
				y = int(y - 0.1*h) if int(y - 0.1*h)>0 else 0
				w = int(w + 0.2*w) if int(w + 0.2*w)<w_frame else w_frame-1
				h = int(h + 0.2*h) if int(h + 0.2*h)<h_frame else h_frame-1
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 5)
				face_crop = frame[y:y + h, x:x + w]
				face_crop = cv2.resize(face_crop, (48, 48))
				face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
				face_crop = face_crop.astype('float32') / 255
				face_crop = np.asarray(face_crop)
				face_crop = face_crop.reshape(1, 1, face_crop.shape[0], face_crop.shape[1])
				targets.append(target[np.argmax(model.predict(face_crop))])
			i = i+1

		else:
			break

	diction = {}
	for (i, value) in enumerate(targets):
		diction[str(i)] = str(value)

	js = json.dumps(diction)

	cap.release()

	return js

@app.route('/emotion', methods = ['GET','POST'])
def check_emotions():
    if request.method == 'GET':
        print('GET Request')
        return predict_face_expression()
    
    if request.method == 'POST':
        if request.files:
            file = request.files['videoFile']
            if file.filename == '':
                print('Not filename')
                return "filename not exist"
            else:
                file.save('./temp/' + file.filename)
                print('done')
                return predict_face_expression('temp/'+str(file.filename))
        else:
            print('Not found')
            return "Bhai nahi ayi"
