import numpy as np
from scipy.io import wavfile
import six
import tensorflow as tf
import vggish_input

class OutEmbeddings:
	def __init__(self):
  		self.wav_file = ""
  		self.graph = tf.Graph()
  		self.Session = tf.Session(graph = self.graph)
  		with self.graph.as_default():
  			self.saver = tf.train.import_meta_graph('model/vggish_graph.meta')
  			self.saver.restore(self.Session, 'model/vggish_model.ckpt')
  			self.features_tensor = self.graph.get_tensor_by_name('vggish/input_features:0')
  			self.embedding_tensor = self.graph.get_tensor_by_name('vggish/embedding:0')

	def run(self, wav_file):
		self.examples_batch = vggish_input.wavfile_to_examples(wav_file)

		[self.embedding_batch] = self.Session.run([self.embedding_tensor],feed_dict={self.features_tensor: self.examples_batch})
		return self.embedding_batch
