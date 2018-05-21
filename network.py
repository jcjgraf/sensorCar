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

	dataSet = None

	def __init__(self, dffShape, dataSet=False):
		"""

		"""
		self.dff = FullyConnected(dffShape)

		if dataSet is not False:
			self.dataSet = dataSet

	def train(self, epochs=1, learningRate=0.3):
		"""
			Train dff with the trainingDataSetPath where inputLabelNumber
			determines the number of inputvalues and labelvalues.
			Forthermore optional epochs (default = 1) and learningRate (defualt
			= 0.3) can be specified.
			If no trainingDataSetPath or testDataSetPatht exist they will be
			created
		"""

		print("Training started")
		for epoch in range(epochs):

			print("Epoch {}/{}".format(epoch + 1, epochs))

			# Read trainingfile and train on it line by line
			with open(self.dataSet.trainingDataSetPath, "r") as trf:

				for line in trf:
					# Split the line entities into an array and normalize it
					lineEntities = self.normalize(np.array([float(i) for i in line.split("\t")]))

					inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]
					labels = lineEntities[-self.dataSet.inputLabelNumber[1]:]

					self.dff.train(inputs, labels, learningRate)

				self.getPerformance()

		print("Finished training during {} epochs".format(epochs))

	def evaluate(self, inputVector):
		"""
			Evaluates a given inputVector in the dff and returns the ouputVector
		"""

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

				lineEntities = self.normalize(np.array([float(i) for i in line.split("\t")]))

				inputs = lineEntities[:self.dataSet.inputLabelNumber[0]]
				labels = lineEntities[-self.dataSet.inputLabelNumber[1]:]

				outputs = self.dff.evaluate(inputs)

				# print("o: {},\nl: {},\nd: {}\n{}".format(outputs, labels, np.abs(np.subtract(outputs, labels)), 15 * "-"))

				differenceSum += np.abs(np.subtract(outputs, labels))

				numberOfLines += 1

			print("The mean difference is {}".format(differenceSum / numberOfLines))
