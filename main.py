#! /usr/bin/env python3

"""
	Main script of the sensorCar project. Interpreting this file will start up
	the socket server, neural network etc. Depending on whether we need to load,
	save etc. a trained network this file has to be altered
"""

from network import Network
from dataSet import DataSet
from sensorCarController import SensorCarController
from activationFunction import ActivationFunction

from multiprocessing import Pool


def runCar(networkPath):

	network = Network()
	network.loadNet(networkPath)
	# todo temporarly fix
	network.dff.activation = ActivationFunction.tanh
	sensorCarController = SensorCarController(network)
	sensorCarController.startServer()


def processTrainNetwork(data):
	trainNetwork(data[0], data[1], data[2], data[3])


def trainNetwork(hiddenLayerShape, learningRate, dataSetPath, epochs):

	dataSet = DataSet(dataSetPath, [3, 1])
	network = Network([3] + hiddenLayerShape + [1], ActivationFunction.tanh, dataSet)
	network.train(epochs=epochs, learningRate=learningRate, verbosity=10, saveNet=10)


if __name__ == '__main__':

	# trainNetwork([20], 0.03, "./simulation/dataset/trackMaster.txt", 100)

	runCar("./savedNet/3-100-50-10-1-0_001-trackMaster/440.txt")
