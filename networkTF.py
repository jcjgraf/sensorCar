"""

"""

import functools

import numpy as np
import tensorflow as tf
import os
import time

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


	def __init__(self, shape, dataSet=None):
		self.shape = shape

		if dataSet is not None:
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

	def train(self, epochs=1, learningRate=0.3, verbosity=1, saveStep=None):

		# Check if training possible
		if self.dataSet is None:
			print("Training not possbile since no dataSet is assigned")
			return

		print("{0}\nTraining started\nnumberOfEpochs: {1}".format(15 * "-", epochs))

		if saveStep is not None:
			ds = self.dataSet.fullDataSetPath

			self.savePath = "./savedNetTF/" + "".join(str(e) + "-" for e in self.shape) + str(learningRate).replace('.', '_') + "-" + ds[ds.rfind("/") + 1: ds.rfind(".")] + "/"

			while os.path.exists(self.savePath):
				self.savePath = self.savePath[:self.savePath.rfind("/")] + "I" + self.savePath[self.savePath.rfind("/"):]

			os.makedirs(self.savePath)

			self.saver

		startTrainingTime = time.time()  # Used for calculating used time
		costList = []  # Holds the cost value of each epoch

		deltaEpochTrainingTime = 0  # time between two epochs

		deltaPrintTrainingTime = 0  # time between two prints
		previousPrintTrainingTime = time.time()  # time of the previous print. Used for calculating the deltaPrintTime

		deltaEpochCost = 0
		previousEpochCost = 0

		deltaPrintCost = 0
		previousPrintCost = 0

		for epoch in range(epochs):

			with open(self.dataSet.trainingDataSetPath, "r") as trf:

				costSum = 0  # costSum of one epoch
				numberOfLines = 0

				startEpochTrainingTime = time.time()

				doPrint = False

				# Determine whether this epoch data should be printed
				if verbosity is not 0 and ((epoch + 1) % verbosity == 0 or epoch == 0):

					print("{2}\nEpoch {0}/{1}".format(epoch + 1, epochs, 15 * "-"))

					doPrint = True

				for line in trf:
					print("Process line")
					lineEntities = np.array([float(i) for i in line.split(",")], dtype=np.float128)
					inputs = np.array(lineEntities[:self.dataSet.inputLabelNumber[0]], ndmin=2)
					labels = np.array(np.divide(lineEntities[-self.dataSet.inputLabelNumber[1]:], 25), ndmin=2)

					self.sess.run(self.optimizer(learningRate), feed_dict={self.x: inputs, self.y: labels})

					costSum += self.sess.run(self.loss, feed_dict={self.x: inputs, self.y: labels})

					numberOfLines += 1

			costList.append(costSum / numberOfLines)

			cost = costSum / numberOfLines

			deltaEpochCost = previousEpochCost - cost
			previousEpochCost = cost

			if doPrint:

				deltaTrainingTime = time.time() - startTrainingTime

				deltaEpochTrainingTime = time.time() - startEpochTrainingTime

				deltaPrintTrainingTime = time.time() - previousPrintTrainingTime
				previousPrintTrainingTime = time.time()

				deltaPrintCost = previousPrintCost - cost
				previousPrintCost = cost

				print("{0}{1}{0}".format(5 * "-", self.shape))
				print("deltaTrainingTime:\t{},\ndeltaEpochTrainingTime:\t{},\ndeltaPrintTrainingTime:\t{},\ncost:\t{},\ndeltaEpochCost:\t{},\ndeltaPrintCost:\t{}".format(deltaTrainingTime, deltaEpochTrainingTime, deltaPrintTrainingTime, cost, deltaEpochCost, deltaPrintCost))

			# if printStep and (step == 0 or step == epochs or step % printStep == 0):
			# 	print(step, self.sess.run(self.loss, feed_dict={self.x: xData, self.y: yData}))

			if saveStep is not None and ((epoch == 0) or (epoch == epochs - 1) or epoch % saveStep == 0):
				self.doSave(epoch)

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

		return tf.train.Saver(max_to_keep=10000)

	# def evaluate(self, xData, yData):
		# return self.sess.run(self.loss, feed_dict={self.x: xData, self.y: yData})
	def evaluate(self, xData):
		return self.getPrediction(xData)

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


