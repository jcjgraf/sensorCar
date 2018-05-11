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

	def __init__(self, networkShape, datasetPath=False, datasetInputLabelRatio=False):
		"""
			Init FullyConnected network and if a datasetPath and datasetInputLabelRatio is
			provided, also a DataSet
		"""

		self.net = FullyConnected(networkShape)

		if datasetPath and datasetInputLabelRatio:

			self.dataset = DataSet(datasetPath, datasetInputLabelRatio)

	def prepareForTraining(self):
		"""
			Prepare the dataset if not already done. If no dataset is initialized,
			false is returned, else true
		"""

		# If no dataset is initialized, return
		if self.dataset is None:
			return False

		self.dataset.prepareDataset()

		return True

	def trainNetwork(self, epochs=1):
		"""
			Train network, buto nly if a dataset is initialized. An optional
			epochs parameter can be given
		"""

		# If no dataset is initialized, training is not possible
		if self.prepareForTraining() is False:
			print("No dataset initialized. Training not possible")
			return

		print("Training network")

		for epoch in range(epochs):

			print("Epoch {}".format(epoch + 1))

			# Get the training entities line by line and train the network with them
			line = 1  # Starts with index 1 not 0

			lineEntities = self.dataset.getInputLableEntity(line)

			# While we are not at the end of the list
			while lineEntities is not False:

				self.net.train(lineEntities[0], lineEntities[1])

				line += 1

				lineEntities = self.dataset.getInputLableEntity(line)

		print("Finished training")

	def evaluateMetering(self, sensorInputs):

		return self.net.evaluate(np.array(sensorInputs))


if __name__ == '__main__':

	path = "./simulation/dataset/track636613955649037100.txt"

	sensorCar = SensorCarNetwork([3, 10, 1], path, [3, 1])

	sensorCar.trainNetwork()
