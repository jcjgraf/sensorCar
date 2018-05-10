#! /usr/bin/env python3

"""
	Class represenging a fullyConnected artificial network. At initialisation a
	list where each elements represents the number of neurons in each layer.
	With the evaluate function a given input can be evaluated and with train the
	network can be trained
"""

import numpy as np


class FullyConnected():
	"""
		Class represenging a fullyConnected artificial network. At
		initialisation a list where each elements represents the number of
		neurons in each layer. With the evaluate function a given input can be
		evaluated and with train the network can be trained
	"""

	def __init__(self, shape, learningRate):
		"""
			shape is the array, where each element represents the number of
			fully connected nodes in a specific layer.
		"""

		self.shape = np.array(shape)
		self.size = len(shape)

		# TODO Gaussian Normal distribution
		self.weights = [np.random.randn(y, x) for x, y in zip(self.shape[:-1], self.shape[1:])]

		self.learningRate = learningRate

	def evaluate(self, inputVector, getLayerValues=False):
		"""
			Takes a vector with shape (1, n) as a input, transpose it to shape
			(n, 1) evaluates it in the neural network and returns eighter the
			ouput layer vector or a tuple containing the output vector of shape
			(n, 1) and a matrix containing all ouputs of the neural network
			depending whether getLayerValues is true or false
		"""

		layerVector = inputVector.reshape(len(inputVector), 1)

		networkOutputs = [inputVector]

		# For all layers n (except in input layer) sum up the weights commecting layer n and n-1 times ouput of layer n-1 and pass the output as the new input to the next layer
		for layerWeights in self.weights:

			# Sum up all the inputs * weights for all node in layer n
			summed = np.dot(layerWeights, layerVector)

			# Apply the sigmoid function to the summed input in order to get the output of layer n
			layerVector = self.sigmoid(summed)

			networkOutputs.append(layerVector)

		if getLayerValues:
			return (layerVector, networkOutputs)

		return layerVector

	def train(self, inputs, targetValue):
		"""
			inputs in a inputlayer vector, where targetValue is a vector holding
			the associated lables. A deltaError is calculated and the weights
			are updated
		"""

		# Bring vectors to the right shape: (n, 1)
		inputs = inputs.reshape(len(inputs), 1)

		# TODO check
		targetValue = targetValue.reshape(len(np.ravel(targetValue)), 1)

		# Get the outputs tuple of the network
		networkOutputs = self.evaluate(inputs, True)

		networkErrors = self.backpropagate(networkOutputs[0], targetValue)

		# Iterate over the network, calculate deltaError and update the weights
		for index in range(self.size - 1):
			errorL0 = networkErrors[len(networkErrors) - 1 - index]
			outputL0 = networkOutputs[1][len(networkOutputs[1]) - 1 - index]
			outputL1 = networkOutputs[1][len(networkOutputs[1]) - 2 - index]

			# dE Formula: np.dot(-errorL0 * outputL0 * (1.0 - outputL0), outputL1.T))

			# Update weights
			# same as self.weights[-index] which doesn't work for some reason
			deltaWeight = self.learningRate * np.dot(-errorL0 * outputL0 * (1.0 - outputL0), outputL1.T)

			self.weights[len(self.weights) - 1 - index] -= deltaWeight

		# todo Check if performance improved with the new weights. If so save the new weights, if not restore the old ones

	def backpropagate(self, networkOutput, targetValue):
		"""
			Takes the realValue vector and setValue vector of the output,
			computes the error of the output and backpropagages it, returning a
			list showing the error of each node
		"""

		# Calculate error at the output layer
		error = np.array(targetValue - networkOutput)

		# List containing arrays of the errors of all nodes from inputLayer to the outputLayer
		errorVector = [error]

		# Start at the ouput player and go backwards to the input layer
		for layerWeights in reversed(self.weights):
			# Get layernodes error
			error = np.dot(layerWeights.T, error)

			# Prepend (since we start at the outputlayer and move to the input layer) error to the errorVector
			errorVector.insert(0, error)

		return np.array(errorVector)

	def sigmoid(self, z):
		"""
			Applies the sigmoid function elementvise to the vector z with shape
			(1, n) or (n, 1) and return a vector of the same shape
		"""
		return 1.0 / (1.0 + np.exp(-z))

	def saveWeights(self, path):
		"""
			Saves weights as a binary file to a given path
		"""

		# TODO check if file already exists
		print("Saving weights to {}".format(path))
		np.save(path, self.weights)

	def loadWeights(self, path):
		"""
			Load weights from a binary file from a given path
		"""

		print("Attempting to loading weights from {}".format(path))
		try:
			self.weights = np.load(path)  # todo make sure that the loaded weights match the shape
			print("Successfully loaded weights")
		except Exception as error:
			print("Failed to load file: {}".format(error))
