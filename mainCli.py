#! /usr/bin/env python3

"""
	Main script of the sensorCar project. Interpreting this file will start up
	the socket server, neural network etc. Depending on whether we need to load,
	save etc. a trained network this file has to be altered
"""
from network import Network
from activationFunction import ActivationFunction
from networkTF import NetworkTF
from dataSet import DataSet
from sensorCarController import SensorCarController

from argparse import ArgumentParser

import tensorflow as tf
import os
import re

from experimentNetTF import ExperimentNetTF
from multiprocessing import Pool

parser = ArgumentParser()
parser.add_argument('-n','--network',
	dest='networktype',
	choices=['np', 'tf'],
	default='tf',
	help='determine whether the network should be numpy or tensorflow based')

parser.add_argument('-l','--learningrate',
	dest='learningrate',
	default=0.3,
	type=float,
	help='learningrate used in conjunction with --training')

parser.add_argument('-e','--epochs',
	dest='epochs',
	default=1,
	type=int,
	help='epochs used in conjunction with --training')


parser.add_argument('-s','--shape',
	dest='shape',
	nargs='+',
	type=int,
	help='shape used in conjunction with --training')


group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-t','--training',
	dest='datasetpath',
	nargs=1,
	# metavar='Datasetpath',
	help='Path to the dataset for training mode')
group.add_argument('-d','--drive',
	dest='networkpath',
	nargs=1,
	# metavar='Networkpath',
	help='Path to the network model file drive mode')

args = parser.parse_args()

def runCar(networkPath, networkType):
	print(networkPath)
	start = re.search("/\d", networkPath).start() + 1
	end = re.search("\d_", networkPath).start() - 1
	shape = [int(e) for e in networkPath[start:end].split("-")]

	network = None

	if networkType == 'np':
		network = Network()
		network.loadNet(networkPath)

	elif networkType == 'tf':
		network = NetworkTF(shape)
		network.doLoad(networkPath)

	sensorCarController = SensorCarController(network)
	sensorCarController.startServer()

def trainNetwork(shape, learningRate, dataSetPath, epochs, networkType):

	dataSet = DataSet(dataSetPath, [shape[0], shape[-1]])

	if networkType == 'np':
		network = Network(shape, ActivationFunction.tanh, dataSet)
		network.train(epochs=epochs, learningRate=learningRate, verbosity=10, saveNet=10)

	elif networkType == 'tf':
		network = NetworkTF(shape, learningRate=learningRate, dataSet=dataSet)
		network.train(epochs=epochs, verbosity=10, saveStep=10)

if __name__ == '__main__':
	print(args)

	if args.datasetpath:
		if args.shape is None:
			parser.error("--training requires --shape")

		else:
			print(args.shape)
			trainNetwork(args.shape, args.learningrate, args.datasetpath[0], args.epochs, args.networktype)

	elif args.networkpath:
		runCar(args.networkpath[0], args.networktype)