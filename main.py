#! /usr/bin/env python3

"""

"""

import sys

sys.path.insert(0, '../neuralNetworks/')
sys.path.insert(0, '../neuralNetworks/fullyConnected/')

from fullyConnected import FullyConnected
from dataSet import DataSet

import numpy as np


class SensorCarNetwork():
	"""
		net
	"""

	def __init__(self, networkShape, dataSetPath=False, dataSetInputLabelRatio=False):
		"""
			Init FullyConnected network and if a dataSetPath and dataSetInputLabelRatio is
			provided, also a DataSet
		"""

		self.net = FullyConnected(networkShape)

		if dataSetPath and dataSetInputLabelRatio:

			self.dataSet = DataSet(dataSetPath, dataSetInputLabelRatio)

	def prepareForTraining(self):
		"""
			Prepare the dataSet if not already done. If no dataSet is initialized,
			false is returned, else true
		"""

		# If no dataSet is initialized, return
		if self.dataSet is None:
			return False

		self.dataSet.prepareDataSet()

		return True

	def trainNetwork(self, epochs=1):
		"""
			Train network, but only if a dataSet is initialized. An optional
			epochs parameter can be given
		"""

		# If no dataSet is initialized, training is not possible
		# if self.prepareForTraining() is False:
		# 	print("No dataSet initialized. Training not possible")
		# 	return

		print("Training network")

		for epoch in range(epochs):

			print("Epoch {}".format(epoch + 1))

			# Get the training entities line by line and train the network with them
			line = 1  # Starts with index 1 not 0

			lineEntities = self.dataSet.getInputLableEntity(line, self.dataSet.trainingDataSetPath)

			# While we are not at the end of the list
			while lineEntities is not False:

				self.net.train(lineEntities[0], lineEntities[1])

				line += 1

				lineEntities = self.dataSet.getInputLableEntity(line, self.dataSet.trainingDataSetPath)

		print("Finished training")

	def getPerformance(self):
		"""
			Calculates the performance of the network
		"""

		with open(self.dataSet.testDataSetPath, "r") as f:

			differences = []

			for line in f:

				# An error is thrown when there is an empty line in the dataSet
				try:

					# split line entites into inputs and labels array
					lineEntities = np.array([float(i) for i in line.split("\t")])
					inputs = lineEntities[:self.dataSet.inputLabelRatio[0]]
					labels = lineEntities[-self.dataSet.inputLabelRatio[1]:]

					# Evaluate inputs
					outputs = self.evaluateMetering(inputs)

					differences.append(np.subtract(outputs, labels))

				except Exception as e:
					raise e

			deltaError = np.average(np.array(differences))

			print("dError", deltaError)

	def evaluateMetering(self, sensorInputs):
		"""
			Takes the sensorInputs vector and returns the evaluated output layer
			vector
		"""

		return self.net.evaluate(np.array(sensorInputs))


if __name__ == '__main__':

	path = "./simulation/dataSet/track636613955649037100.txt"

	sensorCar = SensorCarNetwork([3, 10, 1], path, [3, 1])
	sensorCar.dataSet.generateTrainingTestSets([9, 1])

	sensorCar.getPerformance()

	sensorCar.trainNetwork()

	sensorCar.getPerformance()
