from vggish_inference_demo import OutEmbeddings
import os
import pandas as pd
import numpy as np
from keras.models import model_from_json
import matplotlib.pyplot as plt
from statistics import mean

file = '/home/rohit/IIIT-prayagraj/speeks/Speech-Emotion-Analyzer/bothra-sample.wav'
Oeg = OutEmbeddings()

x = Oeg.run(file)

div = 1

xx = []

for i in range((len(x)//div)):
	xx.append(list(np.mean(x[i:i+div], axis = 0)))

xx = np.array(xx).reshape(-1,1,128)

# print(xx)

json_file = open('model/confidence_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("model/confidence_model.h5")

out = np.array(loaded_model.predict(np.array(xx)))

y = []

for i in range(out.shape[0]):
	y.append(np.argmax(out[i]))

y = np.repeat(np.array(y),div)

print(y)

plt.plot(range(y.shape[0]), y)

plt.show()