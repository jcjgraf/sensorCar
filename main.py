#! /usr/bin/env python3

"""
	Main script of the sensorCar project. Interpreting this file will start up
	the socket server, neural network etc. Depending on whether we need to load,
	save etc. a trained network this file has to be altered
"""

import sys
sys.path.insert(0, '../neuralNetworks/')

from network import Network
from dataSet import DataSet
from sensorCarController import SensorCarController
from activationFunction import ActivationFunction


def runCar():
	networkPath = "../neuralNetworks/savedNet/3-100-50-10-1-0_001/100.txt"

	network = Network()
	network.loadNet(networkPath)
	sensorCarController = SensorCarController(network)
	sensorCarController.startServer()


def trainNetwork():
	dataSetPath = "./simulation/dataset/trackMaster.txt"
	hiddenLayerShape = []

	dataSet = DataSet(dataSetPath, [3, 1])
	network = Network([3] + hiddenLayerShape + [1], ActivationFunction.tanh, dataSet)
	network.train(epochs=1, learningRate=0.3, verbosity=1, saveNet=5)


if __name__ == '__main__':
	
	runCar()
