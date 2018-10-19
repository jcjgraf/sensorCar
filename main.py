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
	trainNetwork(data[0], data[1], data[2], data[3])


def trainNetwork(hiddenLayerShape, learningRate, dataSetPath, epochs):

	# dataSet = DataSet(dataSetPath, [3, 1])
	dataSet = DataSet(dataSetPath, [11, 1])
	network = Network([11] + hiddenLayerShape + [1], ActivationFunction.tanh, dataSet)
	network.train(epochs=epochs, learningRate=learningRate, verbosity=10, saveNet=10)


if __name__ == '__main__':

	# ds = "./simulation/dataset/trackMaster.txt"

	# data = [([100, 50, 10], 0.01, ds, 300), ([100, 50, 10], 0.0001, ds, 300), ([100, 50, 10], 0.006, ds, 300), ([100, 50, 10], 0.06, ds, 300)]

	# data = [([100, 50, 10], 0.001, ds, 1000)]

	# data = [([20], 0.3, ds, 300), ([20, 20], 0.03, ds, 300), ([20, 20, 20], 0.003, ds, 300), ([20, 20, 20, 20], 0.0003, ds, 300)]

	# data = [([5], 0.3, ds, 300), ([50], 0.3, ds, 300), ([80], 0.3, ds, 300), ([120], 0.3, ds, 300), ([200], 0.3, ds, 300)]

	# ds = "./simulation/dataset/trackMaster"

	# data = [([100, 50, 10], 0.001, ds + "1k.txt", 300), ([100, 50, 10], 0.001, ds + "2k.txt", 300), ([100, 50, 10], 0.001, ds + "4k.txt", 300), ([100, 50, 10], 0.001, ds + "7k.txt", 300)]

	# ds = "./simulation/datasetII/randomTrack636743334676676450.txt"

	# data = [([100, 50, 10], 0.001, ds, 500), ([200, 75, 10], 0.001, ds, 500), ([50, 25, 10], 0.001, ds, 500), ([250, 100, 10], 0.001, ds, 500)]

	# p = Pool()
	# p.map(processTrainNetwork, data)

	runCar("./savedNet/11-50-25-10-1-0_001-randomTrack636743334676676450/490.txt")

	
