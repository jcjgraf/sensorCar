"""

"""

import functools

import numpy as np
import tensorflow as tf

class NetworkTF:

	def propertyWithCheck(inputFunc):
		attribute = "_cache_" + inputFunc.__name__

		@property
		@functools.wraps(inputFunc)
		def check_attr(self):
			if not hasattr(self, attribute):
				setattr(self, attribute, inputFunc(self))
			return getattr(self, attribute)

		return check_attr


	def __init__(self, shape):
		self.shape = shape

		self.x = tf.placeholder(tf.float32, shape=[None, self.shape[0]])
		self.y = tf.placeholder(tf.float32, shape=[None, self.shape[-1]])

		self.learningRate = 0.5
		self.numEpochs = 5000

		self.weights = self._getInitWeights()

		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())

		self.predict
		self.optimizer
		self.loss

	def train(self, xData, yData):
		for step in range(self.numEpochs):

			self.sess.run(self.optimizer, feed_dict={self.x: xData, self.y: yData})

			# if step == 0 or step % 10 == 0:
			# 	print(step, self.sess.run(self.loss, feed_dict={self.x: xData, self.y: yData}))

	def _getInitWeights(self):
		return [tf.Variable(tf.truncated_normal([fromLayer, toLayer], stddev=0.1, name="weight{}".format(i))) for i, (fromLayer, toLayer) in enumerate(zip(self.shape[:-1], self.shape[1:]))]

	@propertyWithCheck
	def predict(self):
		layerInput = self.x

		for weight in self.weights:
			layerInput = tf.math.tanh(tf.matmul(layerInput, weight))

		return layerInput

	@propertyWithCheck
	def loss(self):
		# self._loss = tf.square(self.y - self.predict)
		return tf.reduce_mean(tf.square(self.y - self.predict))

	@propertyWithCheck
	def optimizer(self):
		return tf.train.GradientDescentOptimizer(self.learningRate).minimize(self.loss)

	def evaluate(self, xData, yData):
		return self.sess.run(self.predict, feed_dict={self.x: xData})

		# return self.sess.run(self.loss, feed_dict={self.x: xData, self.y: yData})

if __name__ == '__main__':

	networkTF = NetworkTF([2, 3, 1])

	xData = np.array([[0.01, 0.01], [0.01, 0.99], [0.99, 0.99], [0.99, 0.01]])
	yData = np.array([[0.99], [0.01], [0.99], [0.01]])

	networkTF.train(xData, yData)
	print(networkTF.evaluate(np.array([[.99, .99]]), np.array([[1]])))


