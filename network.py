"""
	Network acts like a wrapper for an artificial neural network. (atm only
	dff). Is used for evaluating a net. Compined with a dataSet instance it can
	be used to train and get the performance of the net.
"""

import sys
sys.path.insert(0, '../neuralNetworks/fullyConnected/')

import numpy as np
import matplotlib.pyplot as plt
import pickle

from fullyConnected import FullyConnected


class Network():
	"""
		Network acts like a wrapper for an artificial neural network. (atm only
		dff). Is used for evaluating a net. Compined with a dataSet instance it
		can be used to train and get the performance of the net.
	"""

	dataSet = None

	def __init__(self, dffShape, dataSet=False):
		"""
			dffShape is a array where each element represents the number of
			nodes in each layer of the dff. dataSet is an instance of DataSet.
			When it is not provided network cannot be used to train and get the
			performance of the net
		"""
		self.dff = FullyConnected(dffShape)

		if dataSet is not False:
			self.dataSet = dataSet

	def train(self, epochs=1, learningRate=0.3):
		"""
			If a dataSet is initiated and assigned the dff is trained. An
			optional epochs (Default is 1) and learningRate (Defualt is 0.3) can
			be given
		"""

		if self.dataSet is None:
			print("Training not possbile since no dataSet is assigned")
			return

		print("Training started")

		# Holds the cost value of each epoch
		costList = []

		for epoch in range(epochs):

			print("Epoch {}/{}".format(epoch + 1, epochs))

			# Read trainingfile and train on it line by line
			with open(self.dataSet.trainingDataSetPath, "r") as trf:

				costSum = 0
				numberOfLines = 0

				for line in trf:
					# Split the line entities into an array and normalize it

					# lineEntities = self.normalize(np.array([float(i) for i in line.split("\t")], dtype=np.float128))

					lineEntities = np.array([float(i) for i in line.split("\t")], dtype=np.float128)

					inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]

# todo Normalisation
					# labels = self.normalize(lineEntities[-self.dataSet.inputLabelNumber[1]:])
					labels = (lineEntities[-self.dataSet.inputLabelNumber[1]:])

					costSum += self.dff.train(inputs, labels, learningRate)

					numberOfLines += 1

				costList.append(costSum[0][0] / numberOfLines)

				print("cost: {}".format(costSum / numberOfLines))

		print("Finished training during {} epochs".format(epochs))

		plt.plot(costList)
		plt.show()

	def evaluate(self, inputVector, normalize=False):
		"""
			Evaluates a given inputVector in the dff and returns the ouputVector
		"""

# todo Normalisation
		# if normalize:
		# 	# Normalize input
		# 	# inputVector = self.normalize(inputVector)

		# 	# Evaluate
		# 	outputVector = self.dff.evaluate(inputVector)

		# 	return outputVector

		# 	# Normalize output
		# 	return self.normalize(outputVector)

		return self.dff.evaluate(inputVector)

	def normalize(self, vector):
		"""
			Normalizes the vector by return a vector with the reciprocal value
			of each element in vector
		"""

		return np.divide(1, vector, out=np.zeros_like(vector), where=vector != 0)

	def getPerformance(self):
		"""
			Evaluate how well the net does by taking the abs value of the
			subtraction of the lable by the evaluated value
		"""

		# Open the testDataSetPath and calculate the difference line by line
		with open(self.dataSet.testDataSetPath, "r") as tef:

			# Used for calculating the mean
			numberOfLines = 0
			differenceSum = 0.0

			# Get the difference line by line and add it to the differenceSum
			for line in tef:

				# lineEntities = self.normalize(np.array([float(i) for i in line.split("\t")], dtype=np.float128))

				lineEntities = np.array([float(i) for i in line.split("\t")], dtype=np.float128)

				inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]

# todo Normalisation
				# labels = self.normalize(lineEntities[-self.dataSet.inputLabelNumber[1]:])
				labels = (lineEntities[-self.dataSet.inputLabelNumber[1]:])

				outputs = self.dff.evaluate(inputs)[0][0]

				differenceSum += np.abs(np.subtract(outputs, labels))

				numberOfLines += 1

			print("The mean difference is {}".format(differenceSum / numberOfLines))

	def save(self, filePath):
		"""
			Save the instance of this class to the given filePath
		"""

		print("Saving network instance to {}".format(filePath))

		with open(filePath, "wb") as f:
			f.write(pickle.dumps(self.__dict__))

	def load(self, filePath):
		"""
			Load the instance of this class from the given filePath
		"""

		print("Loading network instance from {}".format(filePath))

		with open(filePath, "rb") as f:
			self.__dict__ = pickle.load(f)
