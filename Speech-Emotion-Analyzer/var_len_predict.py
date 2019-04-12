import librosa
import numpy as np
from keras.models import model_from_json
import keras
import tensorflow as tf
import pandas as pd
import soundfile as sf

# file_name = '/home/rohit/IIIT-prayagraj/speeks/audioset/production/long-sample.wav'

file_name = 'bothra-sample.wav'

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")

opt = keras.optimizers.rmsprop(lr=0.00001, decay=1e-6)

loaded_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

f = sf.SoundFile(file_name)

duration = int(len(f) / f.samplerate)

print("duration:{}".format(duration))

X, sample_rate = librosa.load(file_name, res_type='kaiser_fast',duration=duration,sr=22050*2,offset=0.5)
sample_rate = np.array(sample_rate)
mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
featurelive = mfccs
livedf2 = featurelive

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

list_gender = []
for i in livepreds1:
	list_gender.append(male_calm[i].split('_')[0])
	print(male_calm[i])

print(np.unique(np.array(list_gender), return_counts = True))
