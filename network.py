"""
	Network acts like a wrapper for an artificial neural network. (atm only
	dff). Is used for evaluating a net. Compined with a dataSet instance it can
	be used to train and get the performance of the net.
"""

import numpy as np
import pickle  # Save instance of class
import time  # Measure time

import os

from fullyConnected import FullyConnected


class Network():
	"""
		Network acts like a wrapper for an artificial neural network. (atm only
		dff). Is used for evaluating a net. Compined with a dataSet instance it
		can be used to train and get the performance of the net.
	"""

	dataSet = None

	def __init__(self, dffShape=False, activation=False, dataSet=False):
		"""
			dffShape is a array where each element represents the number of
			nodes in each layer of the dff. dataSet is an instance of DataSet.
			When it is not provided network cannot be used to train and get the
			performance of the net
		"""

		if dffShape and activation:
			self.dff = FullyConnected(dffShape, activation)

		if dataSet is not False:
			self.dataSet = dataSet

	def train(self, epochs=1, learningRate=0.3, verbosity=1, saveNet=None, savePath=None):
		"""
			If a dataSet is initiated and assigned the dff is trained.
			Activation determines the activationfunction and can eigheter be
			"sigmoid" or "tamh". An optional epochs (Default is 1) and
			learningRate (Defualt is 0.3) can be given. Verbosity determines the
			number of epochs after which some information is printed out. The
			optional saveNet is the number of epochs after which the network
			instance is saved to the savePath if provided. Else it will be saved
			to a default path.
			Returns a list containing all costfunction values of each epoch
		"""

		# Check if training possible
		if self.dataSet is None:
			print("Training not possbile since no dataSet is assigned")
			return

		print("{0}\nTraining started\nnumberOfEpochs: {1}".format(15 * "-", epochs))

		if saveNet is not None:

			# Set default filepath if none is provided
			if savePath is None:
				ds = self.dataSet.fullDataSetPath

				savePath = "./savedNet/" + "".join(str(e) + "-" for e in self.dff.shape[0].tolist()) + str(learningRate).replace('.', '_') + "-" + ds[ds.rfind("/") + 1: ds.rfind(".")] + "/"

			# Check if dir already exists, if so add roman letters behinde it
			while os.path.exists(savePath):
				savePath = savePath[:savePath.rfind("/")] + "I" + savePath[savePath.rfind("/"):]

			os.makedirs(savePath)

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

			# Shuffle Dataset
			# self.dataSet.shuffleDataSet(self.dataSet.trainingDataSetPath)

			# Read trainingfile and train on it line by line
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
					# Split the line entities into an array and normalize it
					lineEntities = np.array([float(i) for i in line.split(",")], dtype=np.float128)

					# todo Normalisation
					inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]
					labels = np.divide(lineEntities[-self.dataSet.inputLabelNumber[1]:], 25)
					# labels = lineEntities[-self.dataSet.inputLabelNumber[1]:]

					costSum += self.dff.train(inputs, labels, learningRate)

					numberOfLines += 1

			costList.append(costSum[0][0] / numberOfLines)

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

				print("{0}{1}{0}".format(5 * "-", self.dff.shape))
				print("deltaTrainingTime:\t{},\ndeltaEpochTrainingTime:\t{},\ndeltaPrintTrainingTime:\t{},\ncost:\t{},\ndeltaEpochCost:\t{},\ndeltaPrintCost:\t{}".format(deltaTrainingTime, deltaEpochTrainingTime, deltaPrintTrainingTime, cost, deltaEpochCost, deltaPrintCost))

			if saveNet is not None:
				self.saveTrainingData(savePath + "training.txt", str(cost))

				if (epoch + 1) % saveNet == 0 or epoch == epochs - 1:
					self.saveNet(savePath + str(epoch + 1) + ".txt")

		print("{0}\nepochs: {1},\ncost: {3},\ntrainingTime: {2}\n{0}".format(20 * "-", epochs, time.time() - startTrainingTime, costList[-1]))

		return costList

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

	def getCost(self, inputVector, labelsVector):
		"""
			Returns the MSE
		"""

		return (self.evaluate(inputVector) - labelsVector)**2

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

				# lineEntities = self.normalize(np.array([float(i) for i in line.sit("\t")], dtype=np.float128))

				lineEntities = np.array([float(i) for i in line.split("\t")], dtype=np.float128)

				inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]

# todo Normalisation
				# labels = self.normalize(lineEntities[-self.dataSet.inputLabelNumber[1]:])
				labels = (lineEntities[-self.dataSet.inputLabelNumber[1]:])

				outputs = self.dff.evaluate(inputs)[0][0]

				differenceSum += np.abs(np.subtract(outputs, labels))

				numberOfLines += 1

			print("The mean difference is {}".format(differenceSum / numberOfLines))

	def saveNet(self, filePath):
		"""
			Save the instance of this class to the given filePath
		"""

		print("Saving network instance to {}".format(filePath))

		with open(filePath, "wb") as f:
			f.write(pickle.dumps(self.__dict__))

	def saveTrainingData(self, filePath, toSave):
		"""
			Saves toSave to the text file specified in the filePath
		"""

		print("Saving network training data to {}".format(filePath))

		with open(filePath, "a") as f:
			f.write("\n" + toSave)

	def loadNet(self, filePath):
		"""
			Load the instance of this class from the given filePath
		"""

		print("Loading network instance from {}".format(filePath))

		with open(filePath, "rb") as f:
			self.__dict__ = pickle.load(f)
