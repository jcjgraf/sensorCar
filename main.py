"""
	SensorCarController combines the fullyConnected ANN and the dataSet in order to
	make the sensorCar in the simulation run. Offers training functionality and
	acts as a wrapper for fullyConnected and dataSet
"""

import sys

sys.path.insert(0, '../neuralNetworks/')
sys.path.insert(0, '../neuralNetworks/fullyConnected/')

from fullyConnected import FullyConnected
from dataSet import DataSet

import numpy as np


class SensorCarController():
	"""
		SensorCarController combines the fullyConnected ANN and the dataSet in
		order to make the sensorCar in the simulation run. Offers training
		functionality and acts as a wrapper for fullyConnected and dataSet
	"""

	def __init__(self, networkShape=False, dataSetPath=False, dataSetInputLabelRatio=False):
		"""
			Init FullyConnected network with an optional networkShape and a
			dataSet if the optional dataSetPath and dataSetInputLabelRatio are
			provided
		"""

		if networkShape is not False:
			self.net = FullyConnected(networkShape)

		if dataSetPath is not False and dataSetInputLabelRatio is not False:
			self.dataSet = DataSet(dataSetPath, dataSetInputLabelRatio)

	def trainNetwork(self, epochs=1):
		"""
			Train network, but only if a network and a a dataSet are initialized.
			An optional epochs parameter can be given
		"""

		# If no dataSet is initialized, training is not possible
		# if self.prepareForTraining() is False:
		# 	print("No dataSet initialized. Training not possible")
		# 	return

		if self.net is None:
			print("No network initiated. Training not prossible")
			return

		if self.dataSet is None:
			print("No dataSet initiated. Training not possible")
			return

		if self.dataSet.trainingDataSetPath is None:
			print("No trainingDataSet generated. Training not possible")
			return

		print("Train network")

		for epoch in range(epochs):

			# TODO shuffle dataSet
			print("Epoch {} / {}".format(epoch, epochs))

			# Get the training entities line by line and train the network with them
			line = 1  # Starts with index 1 not 0
			lineEntities = self.dataSet.getInputLableEntities(line)  # False in case we are at the end of the file

			# While we are not at the end of the list
			while lineEntities is not False:

				self.net.train(lineEntities[0], lineEntities[1])

				line += 1

				lineEntities = self.dataSet.getInputLableEntities(line)

		print("Finished training with {} epochs".format(epochs))

	def getPerformance(self):
		"""
			Calculates the performance of the network with the testDataSet by
			subtracting the lables from the evaluated input vector in the net,
			and calculating the mean of the resulting vector. Returning the
			deltaError
		"""

		if self.net is None:
			print("No network initiated. Calculating performance not prossible")
			return

		if self.dataSet is None:
			print("No dataSet initiated. Calculating performance not possible")
			return

		if self.dataSet.testDataSetPath is None:
			print("No testDataSet generated. Calculating performance not possible")
			return

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

					# Calculate difference by calculating outputs - labels
					differences.append(np.subtract(outputs, labels))

				except Exception as e:
					raise e

			# Average resulting vector
			deltaError = np.average(np.array(differences))

			return deltaError

	def evaluateMetering(self, sensorInputs):
		"""
			Returns the evaluation of the sensorInputs in the network
		"""

		if self.net is None:
			print("No network initiated. Evaluating metering not prossible")
			return

		if self.net.shape is None:
			print("No shape for network set. Evaluating metering not prossible")
			return

		if self.net.size is None:
			print("No size for network set. Evaluating metering not prossible")
			return

		if self.net.weights is None:
			print("No weights for network set. Evaluating metering not prossible")
			return

		# todo check if size matches

		return self.net.evaluate(np.array(sensorInputs))


if __name__ == '__main__':

	path = "./simulation/dataSet/track636613955649037100.txt"

	sensorCar = SensorCarController([3, 10, 1], path, [3, 1])
	sensorCar.dataSet.prepareDataSet()
	sensorCar.dataSet.generateTrainingTestSets()

	print("DeltaError: {}".format(sensorCar.getPerformance()))

	sensorCar.trainNetwork()

	print("DeltaError: {}".format(sensorCar.getPerformance()))
