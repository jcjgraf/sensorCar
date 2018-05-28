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

	path = "/Users/JeanClaude/Documents/Programming/matriculationProject/practical/sensorCar/simulation/dataSet/trackMaster.txt"

	dataSet = DataSet(path, [3, 1], [1, 1])
	network = Network([3, 100, 50, 10, 1], dataSet)

	network.loadNet("../neuralNetworks/savedNet/3-100-50-10-1-0_001/100.txt")

	sensorCarController = SensorCarController(network)

	sensorCarController.startServer()
