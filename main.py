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
	# networkPath = "./savedNet/3-20-1-0_03-trackMaster/460.txt"

	network = Network()
	network.loadNet(networkPath)
	# todo temporarly fix
	network.dff.activation = ActivationFunction.tanh
	sensorCarController = SensorCarController(network)
	sensorCarController.startServer()


def processTrainNetwork(data):
	trainNetwork(data[0], data[1], data[2])


def trainNetwork(hiddenLayerShape, learningRate, dataSetPath):

	# dataSetPath = "./simulation/dataset/trackMaster.txt"

	dataSet = DataSet(dataSetPath, [3, 1])
	network = Network([3] + hiddenLayerShape + [1], ActivationFunction.tanh, dataSet)
	network.train(epochs=500, learningRate=learningRate, verbosity=10, saveNet=10)


if __name__ == '__main__':

	ds = "./simulation/dataset/trackMaster.txt"

	data = [([20], 0.3, ds), ([50], 0.3, ds), ([80], 0.3, ds), ([120], 0.3, ds), ([200], 0.3, ds)]

	p = Pool()
	p.map(processTrainNetwork, data)

	# trainNetwork([100, 50, 10], 0.001, "./simulation/dataset/trackMaster.txt")

	# runCar()

	
