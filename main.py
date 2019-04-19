#! /usr/bin/env python3

"""
	Main script of the sensorCar project. Interpreting this file will start up
	the socket server, neural network etc. Depending on whether we need to load,
	save etc. a trained network this file has to be altered
"""

from network import Network
from networkTF import NetworkTF
from dataSet import DataSet
from sensorCarController import SensorCarController
from activationFunction import ActivationFunction
from experimentNetTF import ExperimentNetTF

from multiprocessing import Pool

import tensorflow as tf
import os
import re


def runCar(networkPath):
	start = re.search("/\d", networkPath).start() + 1
	end = re.search("\d_", networkPath).start() - 1
	shape = [int(e) for e in networkPath[start:end].split("-")]

# Vanilla
	# network = Network()
	# network.loadNet(networkPath)
	# network.dff.activation = ActivationFunction.tanh

# TF
	network = NetworkTF(shape)
	network.doLoad(networkPath)

	sensorCarController = SensorCarController(network)
	sensorCarController.startServer()

def processTrainNetwork(data):
	trainNetwork(data[0], data[1], data[2], data[3])

def trainNetwork(hiddenLayerShape, learningRate, dataSetPath, epochs):

	dataSet = DataSet(dataSetPath, [3, 1])

# Vanilla
	# network = Network([3] + hiddenLayerShape + [1], ActivationFunction.tanh, dataSet)
	# network.train(epochs=epochs, learningRate=learningRate, verbosity=10, saveNet=10)

# TF
	network = NetworkTF([3] + hiddenLayerShape + [1], learningRate=learningRate, dataSet=dataSet)
	network.train(epochs=epochs, saveStep=150, verbosity=0)


if __name__ == '__main__':

	dsPath = "./simulation/dataset/trackMaster"
	ds = "./simulation/dataset/trackMaster.txt"

	data = []

	# 1: Dataset size
	# data += [([100, 50, 10], 0.001, dsPath + "1k.txt", 150), ([100, 50, 10], 0.001, dsPath + "2k.txt", 150), ([100, 50, 10], 0.001, dsPath + "4k.txt", 150), ([100, 50, 10], 0.001, dsPath + "7k.txt", 150), ([100, 50, 10], 0.001, dsPath + ".txt", 150)]

	# 2: Learningrate
	# data += [([100, 50, 10], 0.1, ds, 150), ([100, 50, 10], 0.01, ds, 150), ([100, 50, 10], 0.001, ds, 150), ([100, 50, 10], 0.0001, ds, 150), ([100, 50, 10], 0.00001, ds, 150)]
	# data += [([100, 50, 10], 0.1, ds, 150), ([100, 50, 10], 0.01, ds, 150)]

	# 3: Size
	# data += [([50, 25], 0.001, ds, 150), ([75, 35, 10], 0.001, ds, 150), ([150, 75, 25], 0.001, ds, 150), ([150, 100, 25, 10], 0.001, ds, 150)]
	# data += [([150, 75, 25], 0.001, ds, 1), ([150, 100, 25, 10], 0.001, ds, 1)]

	# 4: Repetition
	# data += [([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150)]
	# data += [([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150),([100, 50, 10], 0.001, ds, 150)]

	p = Pool()
	p.map(processTrainNetwork, data)

	# trainNetwork([10], 0.001, "./simulation/dataset/trackMaster.txt", 200)

	# runCar("./savedNetTF/3-10-1-0_0005-trackMaster1kII/model-9")

