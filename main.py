#! /usr/bin/env python3

"""
	Main script of the sensorCar project
"""

import sys
sys.path.insert(0, '../neuralNetworks/')

from network import Network
from dataSet import DataSet

from sensorCarController import SensorCarController


if __name__ == '__main__':

	path = "./simulation/dataSet/track636614043698560200.txt"

	dataSet = DataSet(path, [3, 1], [1, 1])
	network = Network([3, 10, 1], dataSet)

	sensorCarController = SensorCarController(network)

	sensorCarController.network.getPerformance()
	sensorCarController.network.train(epochs=2, learningRate=0.5)
	sensorCarController.network.getPerformance()

	sensorCarController.startServer()
