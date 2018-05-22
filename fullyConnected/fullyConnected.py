"""
	FullyConnected represents a deep fullyConnected artificial network (dff). At
	initialisation a list where each elements represents the number of neurons
	in each layer. With the evaluate function a given input can be evaluated and
	with train the network can be trained
"""

import numpy as np

# import os.path  # check if a file exists at a certain path


class FullyConnected():
	"""
		FullyConnected represents a deep fullyConnected artificial network
		(dff). At initialisation a list where each elements represents the
		number of neurons in each layer. With the evaluate function a given
		input can be evaluated and with train the network can be trained
	"""

	shape = None
	size = None
	weights = None

	def __init__(self, shape):
		"""
			Initiate network with a shape list, where each element represents
			the number of fully connected nodes in a specific layer.
			For each link weights are created at random.
		"""

		self.shape = np.array(shape, ndmin=2)
		self.size = len(shape)

		# TODO Gaussian Normal distribution
		# self.weights = [np.random.randn(y, x) for x, y in zip(shape[:-1], shape[1:])]

		self.weights = [np.random.normal(0, 0.01, size=(y, x)) for x, y in zip(shape[:-1], shape[1:])]

	def evaluate(self, inputVector, getLayerValues=False):
		"""
			Takes a vector with shape (1, n) as a input, transpose it to shape
			(n, 1) evaluates it in the neural network and returns eighter the
			ouput layer vector or a tuple containing the output vector of shape
			(n, 1) and a list containing all layer's node values (as vectors,
			used in the training method) depending whether getLayerValues is
			true or false (Default is false)
		"""

		layerVector = inputVector.reshape(len(inputVector), 1)

		networkLayerValues = [inputVector]

		# For all layers n (except in input layer) sum up the weights commecting layer n and n-1 times ouput of layer n-1 and pass the output as the new input to the next layer
		for layerWeights in self.weights:

			# Sum up all the inputs * weights for all node in layer n
			summed = np.dot(layerWeights, layerVector)

			# Apply the sigmoid function to the summed input in order to get the output of layer n
			layerVector = self.sigmoid(summed)

			networkLayerValues.append(layerVector)

		# Return eighter a tuple of just the output vector
		if getLayerValues:
			return (layerVector, networkLayerValues)

		return layerVector

	def train(self, inputs, labels, learningRate=0.5):
		"""
			inputs is the inputlayer vector, where labels is a vector holding
			the associated labels. A deltaError is calculated and the weights
			are updated. An optional learningRate can be given (Default is 0.5)
		"""

		# Bring vectors to the right shape: (n, 1)
		inputs = inputs.reshape(len(inputs), 1)
		labels = labels.reshape(len(np.ravel(labels)), 1)

		# Get the outputs tuple of the network
		networkOutputs = self.evaluate(inputs, getLayerValues=True)

		networkErrors = self.backpropagate(networkOutputs[0], labels)

		# Iterate over the network, calculate deltaError and update the weights
		for index in range(self.size - 1):
			errorL0 = networkErrors[len(networkErrors) - 1 - index]
			outputL0 = networkOutputs[1][len(networkOutputs[1]) - 1 - index]
			outputL1 = networkOutputs[1][len(networkOutputs[1]) - 2 - index]

			# dE Formula: np.dot(-errorL0 * outputL0 * (1.0 - outputL0), outputL1.T))

			# Update weights
			# same as self.weights[-index] which doesn't work for some reason
			# deltaWeight = learningRate * np.dot(-errorL0 * outputL0 * (1.0 - outputL0), outputL1.T)  # Sigmoid

			deltaWeight = learningRate * np.dot(-errorL0 * (1.0 - np.square(outputL0)), outputL1.T)  # tanh

			self.weights[len(self.weights) - 1 - index] -= deltaWeight

		# todo Check if performance improved with the new weights. If so save the new weights, if not restore the old ones

	def backpropagate(self, outputs, labels):
		"""
			Takes the outputs vector and labels vector of the output,
			computes the error of the output and backpropagages it, returning a
			list showing the error of each node
		"""

		# Calculate error at the output layer
		error = np.array(labels - outputs)

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
			Applies the sigmoid function elementwise to the vector z with shape
			(1, n) or (n, 1) and return a vector of the same shape
		"""

		# Cast to float128 else we get an overflow error
		z = z.astype(np.float128)

		return (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))  # tanh

		# return 1.0 / (1.0 + np.exp(-z))  # Sigmoid

	# def saveWeights(self, fullFilePath):
	# 	"""
	# 		Saves weights as a binary file to the given fullFilePath.
	# 	"""

	# 	if os.path.exists(fullFilePath):
	# 		print("Network cannot be saved since that file already exists at that path")
	# 		return

	# 	np.save(fullFilePath, self.weights)
	# 	print("Saved weights to {}".format(fullFilePath))

	# def loadWeights(self, fullFilePath):
	# 	"""
	# 		Load weights from a binary file from the given fullFilePath
	# 	"""

	# 	print("Attempting to loading weights from {}".format(fullFilePath))
	# 	try:
	# 		self.weights = np.load(fullFilePath)

	# 		# todo set self.shape and self.size according to retrieved self.weights
	# 		print("Successfully loaded weights and created network")

	# 	except Exception as error:
	# 		print("Failed to load weights: {}".format(error))
