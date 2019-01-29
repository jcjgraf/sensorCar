"""

"""

import functools

import numpy as np
import tensorflow as tf
import os

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

	dataSet = None
	savePath = None


	def __init__(self, shape, dataSet=False):
		self.shape = shape

		if dataSet is not False:
			self.dataSet = dataSet

		# Tensorflow attributes
		self.x = tf.placeholder(tf.float32, shape=[None, self.shape[0]])
		self.y = tf.placeholder(tf.float32, shape=[None, self.shape[-1]])

		self.learningRate = 0.5

		self.weights = self._getInitWeights()

		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())

		self.predict
		# self.optimizer
		self.loss

	def train(self, epochs=1, learningRate=0.3, printStep=None, saveStep=None):

		if saveStep is not None:
			self.savePath = "./savedNetTF/" + "".join(str(e) + "-" for e in self.shape) + str(learningRate).replace('.', '_') + "/"
			self.saver

		for step in range(epochs):

			with open(self.dataSet.trainingDataSetPath, "r") as trf:

				for line in trf:
					lineEntities = np.array([float(i) for i in line.split(",")], dtype=np.float128)

					inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]
					labels = np.divide(lineEntities[-self.dataSet.inputLabelNumber[1]:], 25)

					self.sess.run(self.optimizer(learningRate), feed_dict={self.x: inputs, self.y: labels})

			if printStep and (step == 0 or step == epochs or step % printStep == 0):
				print(step, self.sess.run(self.loss, feed_dict={self.x: xData, self.y: yData}))

			if saveStep is not None and ((step == 0) or (step == epochs - 1) or step % saveStep == 0):
				self.doSave(step)

	def getPrediction(self, xData):
		return self.sess.run(self.predict, feed_dict={self.x: xData})

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
		return tf.reduce_mean(tf.square(self.y - self.predict))

	# @propertyWithCheck
	def optimizer(self, learningRate):
		return tf.train.GradientDescentOptimizer(learningRate).minimize(self.loss)

	@propertyWithCheck
	def saver(self):

		while os.path.exists(self.savePath):
			self.savePath = self.savePath[:self.savePath.rfind("/")] + "I" + self.savePath[self.savePath.rfind("/"):]

		os.makedirs(self.savePath)


		return tf.train.Saver(max_to_keep=10000)

	def evaluate(self, xData, yData):
		return self.sess.run(self.loss, feed_dict={self.x: xData, self.y: yData})

	def doSave(self, step):
		savePath = self.saver.save(self.sess, os.path.join(self.savePath, "model"), global_step = step)
		print("Saved current model to {}".format(savePath))

	def doLoad(self, modelPath):
		self.saver.restore(self.sess, modelPath)
		print("Loaded model from {}".format(modelPath))


if __name__ == '__main__':

	networkTF = NetworkTF([3, 100, 1])

	# xData = np.array([[0.01, 0.01], [0.01, 0.99], [0.99, 0.99], [0.99, 0.01]])
	# yData = np.array([[0.99], [0.01], [0.99], [0.01]])

	networkTF.train(epochs=10, saveStep=10)
	# networkTF.doLoad("./savedNetTF/2-3-1-0_5IIIIIIIIII/model-999")

	print(networkTF.getPrediction(np.array([[.99, .99]])))


