"""

"""

from functools import wraps

import numpy as np
import tensorflow as tf
import os
import shutil
import pathlib
import time

class NetworkTF:

	def propertyWithCheck(inputFunc):
		attribute = "_cache_" + inputFunc.__name__

		@property
		@wraps(inputFunc)
		def check_attr(self):
			if not hasattr(self, attribute):
				setattr(self, attribute, inputFunc(self))
			return getattr(self, attribute)

		return check_attr

	dataSet = None
	savePath = None

	def __init__(self, shape, learningRate=0.3, dataSet=None, tensorboard=None):

		self.tensorboardEnabled = True if tensorboard is not None else False

		tf.reset_default_graph()
		self.shape = shape

		self.learningRate = learningRate

		if dataSet is not None:
			self.dataSet = dataSet

			ds = self.dataSet.fullDataSetPath

			self.uid =  "".join(str(e) + "-" for e in self.shape) + str(self.learningRate).replace('.', '_') + "-" + ds[ds.rfind("/") + 1: ds.rfind(".")]

		else:
			self.uid = "".join(str(e) + "-" for e in self.shape) + str(self.learningRate).replace('.', '_')

		# Tensorflow attributes

		self.x = tf.placeholder(tf.float32, shape=[None, self.shape[0]], name="InputData")
		self.y = tf.placeholder(tf.float32, shape=[None, self.shape[-1]], name="LabelData")

		self.weights = self._getInitWeights()

		self.saver = self.saver()

		self.predict
		self.optimizer
		self.loss

		if self.tensorboardEnabled:
			self.logDir = tensorboard + self.uid + str(int(time.time()))
			pathlib.Path(self.logDir).mkdir(parents=True, exist_ok=True)

			tf.summary.scalar("loss", self.loss)
			self.mergedSummary = tf.summary.merge_all()

		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())

		if self.tensorboardEnabled:
			self.summaryWriter = tf.summary.FileWriter(self.logDir, graph=tf.get_default_graph())

	def train(self, epochs=1, verbosity=1, saveStep=None):

		# Check if training possible
		if self.dataSet is None:
			print("Training not possbile since no dataSet is assigned")
			return

		print("{0}\nTraining started\nnumberOfEpochs: {1}".format(15 * "-", epochs))

		if saveStep is not None:
			ds = self.dataSet.fullDataSetPath

			self.savePath = "./savedNetTF/" + self.uid + "/"

			while os.path.exists(self.savePath):
				self.savePath = self.savePath[:self.savePath.rfind("/")] + "I" + self.savePath[self.savePath.rfind("/"):]

			os.makedirs(self.savePath)

			self.saver

			if saveStep == -1:
				previousCost = 1e309

		startTrainingTime = time.time()  # Used for calculating used time
		costList = []  # Holds the cost value of each epoch

		deltaEpochTrainingTime = 0  # time between two epochs

		deltaPrintTrainingTime = 0  # time between two prints
		previousPrintTrainingTime = time.time()  # time of the previous print. Used for calculating the deltaPrintTime

		deltaEpochCost = 0
		previousEpochCost = 0

		deltaPrintCost = 0
		previousPrintCost = 0

		counter = 0

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

					lineEntities = np.array([float(i) for i in line.split(",")], dtype=np.float128)
					inputs = np.array(lineEntities[:self.dataSet.inputLabelNumber[0]], ndmin=2)
					labels = np.array(np.divide(lineEntities[-self.dataSet.inputLabelNumber[1]:], 25), ndmin=2)

					loss = self.sess.run(self.loss, {self.x: inputs, self.y: labels})

					if self.tensorboardEnabled:
						summary = self.sess.run(self.mergedSummary, {self.x: inputs, self.y: labels})
						self.summaryWriter.add_summary(summary, counter)

					_ = self.sess.run(self.optimizer, {self.x: inputs, self.y: labels})

					costSum += loss

					numberOfLines += 1
					counter += 1

			costList.append(costSum / numberOfLines)

			cost = costSum / numberOfLines

			if saveStep is not None:
				name = self.savePath[:self.savePath.rfind("/")][self.savePath[:self.savePath.rfind("/")].rfind("/") + 1:] + ".txt"

				self.saveTrainingData(self.savePath + name, cost)

			if self.tensorboardEnabled:
				addListSummary = tf.Summary()
				addListSummary.value.add(tag="MeanLoss", simple_value=cost)
				self.summaryWriter.add_summary(addListSummary, epoch)
				self.summaryWriter.flush()

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

			if saveStep is not None and ((epoch == 0) or (epoch == epochs - 1) or epoch % saveStep == 0):
				self.doSave(epoch)

			if saveStep == -1 and (previousCost > cost):
				self.doSave(epoch)
				previousCost = cost

	def getPrediction(self, xData):
		return self.sess.run(self.predict, feed_dict={self.x: xData})

	def _getInitWeights(self):
		return [tf.Variable(tf.truncated_normal([fromLayer, toLayer], stddev=0.1), name="Weight{}".format(i)) for i, (fromLayer, toLayer) in enumerate(zip(self.shape[:-1], self.shape[1:]))]

	@propertyWithCheck
	def predict(self):
		layerInput = self.x

		for weight in self.weights:
			layerInput = tf.math.tanh(tf.matmul(layerInput, weight))

		return layerInput

	@propertyWithCheck
	def loss(self):
		return tf.reduce_mean(tf.square(self.y - self.predict))

	@propertyWithCheck
	def optimizer(self):
		return tf.train.GradientDescentOptimizer(self.learningRate).minimize(self.loss)

	def saver(self):
		return tf.train.Saver(max_to_keep=10000)

	def evaluate(self, xData):
		return self.getPrediction(xData)

	def doSave(self, step):
		savePath = self.saver.save(self.sess, os.path.join(self.savePath, "model"), global_step = step)
		print("Saved current model to {}".format(savePath))

	def doLoad(self, modelPath):
		self.saver.restore(self.sess, modelPath)
		print("Loaded model from {}".format(modelPath))

	def saveTrainingData(self, filePath, toSave):
		# os.makedirs(filePath)

		# print("Saving network training data to {}".format(filePath))

		with open(filePath, "a") as f:
			f.write(str(toSave) + "\n")


