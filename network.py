"""
	Wrapperclass for nets
"""

import sys

sys.path.insert(0, './fullyConnected/')

import numpy as np

# import os.path  # check if a file exists at a certain path

from fullyConnected import FullyConnected


class Network():
	"""
		Wrapperclass for nets
	"""

	trainingDataSetPath = None
	testDataSetPath = None

	def __init__(self, dffShape):
		"""

		"""
		self.dff = FullyConnected(dffShape)

	def train(self, fullDataSetPath, inputLabelNumber, epochs=1, learningRate=0.3):
		"""
			Train dff with the fullDataSetPath where inputLabelNumber determines
			the number of inputvalues and labelvalues in the fullDataSetPath.
			Forthermore optional epochs (default = 1) and learningRate (defualt
			= 0.3) can be specified.
			If no trainingDataSetPath or testDataSetPatht exist they will be
			created
		"""

		# Determine of we have to split the fullDataSetPath first
		if self.trainingDataSetPath is None or self.testDataSetPatht is None:
			print("Has to split the dataset first")
			self.splitDataSet(fullDataSetPath)

		print("Training started")
		for epoch in epochs:

			print("Epoch {}/{}".format(epoch, epochs))

			# Read trainingfile and train on it line by line
			with open(self.trainingDataSetPath, "r") as trf:

				for line in trf:
					lineEntities = np.array([float(i) for i in line.split("\t")])

					inputs = lineEntities[:inputLabelNumber[0]]
					labels = self.normalize(lineEntities[-inputLabelNumber[1]:])  # Labels have to be normalized,

					self.dff.train(inputs, labels, learningRate)

		print("Finished training during {} epochs".format(epochs))

	def evaluate(self, inputVector):
		"""
			Evaluates a given inputVector in the dff and returns the ouputVector
		"""

		return self.dff.evaluate(inputVector)

	def splitDataSet(self, fullDataSetPath, splitRatio=[9, 1]):
		"""
			Split the given fullDataSetPath by the optionally given splitRation
			(default is 9:1) into two files, which are saved in the same path as
			the fullDataSetPath but with the ending "_training.txt" resp.
			"_test.txt"
		"""

		# Get number of lines(=data) in the fullDataSetPath
		numberOfLines = 0

		with open(fullDataSetPath, "r") as ff:
			for line in ff:
				numberOfLines += 1

		self.trainingDataSetPath = fullDataSetPath[:fullDataSetPath.rfind(".")] + "_training.txt"
		self.testDataSetPath = fullDataSetPath[:fullDataSetPath.rfind(".")] + "_test.txt"

		# Get the number of elements for the training set (testset equals the remainder)
		splitRatioSum = float(splitRatio[0] + splitRatio[1])
		numberTrainingEntities = int(round(float(splitRatio[0]) * numberOfLines / splitRatioSum))

		# Split the entites of the fullDataSetPath into the two files
		with open(fullDataSetPath, "r") as ff:

			for (i, line) in enumerate(ff):
				if i < numberTrainingEntities:
					with open(self.trainingDataSetPath, "a") as trf:
						trf.write(line)

				if i >= numberTrainingEntities:
					with open(self.testDataSetPath, "a") as tef:
						tef.write(line)

			print("Created training and test dataSet")

	def normalize(self, vector):
		"""
			Normalizes the vector by return a vector with the reciprocal value
			of each element in vector
		"""

		return np.divide(1, vector, out=np.zeros_like(vector), where=vector != 0)

	def getPerformance(self, inputLabelNumber):
		"""
			Evaluate how well the net does by taking the abs value of the
			subtraction of the lable by the evaluated value
		"""

		# Determine of testDataSetPath exists and whether performance can be obtrained
		if self.testDataSetPath is None:
			print("No testDataSet generated. Calculating performance not possible")
			return

		# Open the testDataSetPath and calculate the difference line by line
		with open(self.testDataSetPath, "r") as tef:

			# Used for calculating the mean
			numberOfLines = 0
			differenceSum = 0.0

			# Get the difference line by line and add it to the differenceSum
			for line in tef:

				lineEntities = self.normalize(np.array([float(i) for i in line.split("\t")]))

				inputs = lineEntities[:inputLabelNumber[0]]
				labels = lineEntities[-inputLabelNumber[1]:]

				outputs = self.dff.evaluate(inputs)

				# print("o: {},\nl: {},\nd: {}\n{}".format(outputs, labels, np.abs(np.subtract(outputs, labels)), 15 * "-"))

				differenceSum += np.abs(np.subtract(outputs, labels))

				numberOfLines += 1

			print("The mean difference is {}".format(differenceSum / numberOfLines))
