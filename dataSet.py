"""
	DataSets is responsible for processing, normalising and providing dataSets
	entires to other classes for training of the network.
"""

import numpy as np
import linecache  # Get a specific line of a file

import os.path  # check if a file exists at a certain path


class DataSet():
	"""
		DataSets is responsible for processing, normalising and providing
		dataSets entires to other classes for training of the network.
	"""

	rawDataSetPath = None
	inputLabelRatio = None
	processedDataSetPath = None
	trainingDataSetPath = None
	testDataSetPath = None

	def __init__(self, rawDataSetPath, inputLabelRatio):
		"""
			Initiate dataSet with a path to the rawDataSet and an array
			representing the ration between inputs and lables
		"""
		# Check if path is valid and file exists
		if os.path.exists(rawDataSetPath):
			self.rawDataSetPath = rawDataSetPath
		else:
			print("Given path is invalid. Reasign right path to attribute")

		self.inputLabelRatio = inputLabelRatio

		# Check if the processedDataSet already exists. If so check if the training- and testDataSet already exist
		# Add for the existing ones the path string as an attribut
		processedDataSetPath = rawDataSetPath[:rawDataSetPath.rfind(".")] + ".scl"

		if os.path.exists(processedDataSetPath):
			self.processedDataSetPath = processedDataSetPath

			trainingDataSetPath = rawDataSetPath[:rawDataSetPath.rfind(".")] + "_training.scl"
			testDataSetPath = rawDataSetPath[:rawDataSetPath.rfind(".")] + "_test.scl"

			if os.path.exists(trainingDataSetPath) and os.path.exists(testDataSetPath):
				self.trainingDataSetPath = trainingDataSetPath
				self.testDataSetPath = testDataSetPath

	def prepareDataSet(self):
		"""
			If no prepared dataSet exists, load the rawDataSet line by line
			and procss this line before saving it to the processedDataSet
			It the moment the procession only includes normalisation
		"""

		# If processedDataSetPath is defined, then there is already a processed dataset
		# There is no need for redoing this. Thus we return
		if self.prepareDataSet is not None:
			print("Prepared dataSet does already exist. No need for recreation.")
			return

		print("Preparing dataSet")

		# Scale DataSet
		# Open file and process it line by line
		with open(self.rawDataSetPath, "r") as f:

			print("Normalising dataSet")

			for line in f:

				# An error is thrown when there is an empty line in the dataSet
				try:

					# split line entites into inputs and labels array
					lineEntities = np.array([float(i) for i in line.split("\t")])
					inputs = lineEntities[:self.inputLabelRatio[0]]
					labels = lineEntities[-self.inputLabelRatio[1]:]

					# Scale inputs/lables
					scaledInputs = self.normalizeInput(inputs)
					scaledLables = self.normalizeInput(labels)

					# Convert float array back to strings
					scaledInputs = [str(i) for i in scaledInputs]
					scaledLables = [str(i) for i in scaledLables]

					# todo make general
					scaledLine = scaledInputs[0] + "\t" + scaledInputs[1] + "\t" + scaledInputs[2] + "\t" + scaledLables[0] + "\n"

					# Save new line to file
					with open(self.processedDataSetPath, "a") as fn:
						fn.write(scaledLine)

				except Exception as e:
					raise e

			print("Finished normalisation")

		print("DataSet is ready")

		# TODO Shuffle DataSet

	def normalizeInput(self, vector):
		"""
			Normalizes the vector by return a vector with the reciprocal value
			of each element in vector
		"""

		return np.divide(1, vector, out=np.zeros_like(vector), where=vector != 0)

	def generateTrainingTestSets(self, trainingTestRatio=[9, 1]):
		"""
			Devides the dataSet into a training and test set by the optionally
			given trainingTestRatio which is an array of two elements.
			Default is [9, 1] meaning 9/10 training and 1/10 testing
		"""

		# If trainingDataSetPath and testDataSetPath is defined, then these two sets already exist
		# There is no need for redoing this. Thus we return
		if self.trainingDataSetPath is not None and self.testDataSetPath is not None:
			print("Training and testDataSet do already exist. No need for recreation.")
			return

		print("Generating training and test dataSet")

		# Get the number of lines in the dataSet by iterating over it. Used for calculating the number in each set
		numberOfLines = 0
		with open(self.rawDataSetPath, "r") as f:
			for line in f:
				numberOfLines += 1

		self.trainingDataSetPath = self.rawDataSetPath[:self.rawDataSetPath.rfind(".")] + "_training.scl"
		self.testDataSetPath = self.rawDataSetPath[:self.rawDataSetPath.rfind(".")] + "_test.scl"

		# Get the number of elements for the training set
		ratioSum = float(trainingTestRatio[0] + trainingTestRatio[1])
		numberOfTraining = int(round(float(trainingTestRatio[0]) * numberOfLines / ratioSum))

		# Split the dataSet according to the calculated number per set
		with open(self.rawDataSetPath, "r") as f:

			for (i, line) in enumerate(f):
				if i < numberOfTraining:
					with open(self.trainingDataSetPath, "a") as tr:
						tr.write(line)

				if i >= numberOfTraining:
					with open(self.testDataSetPath, "a") as te:
						te.write(line)

			print("Created training and test dataSet")

	def getInputLableEntities(self, lineNumber):
		"""
			Loads the line at lineNumber of the dataSet file and returns a tule
			containing an vector of inputs and an lable vector if
			trainingDataSetPath exists.
			False is returned when the lineNumber is "out of range" or
			trainingDataSetPath does not exist.
		"""

		if self.trainingDataSetPath is None:
			print("trainingDataSet does not exist. Not possible to retrieve entities")
			return False

		# Get line at specific index
		line = linecache.getline(self.trainingDataSetPath, lineNumber)  # Returns "" in when the "index is out of range"
		linecache.clearcache()

		if line == "":  # When "index out pf range" an empty string is returned
			return False

		# Create arrays of the line entities. Convert str to float
		lineEntity = np.array([float(i) for i in line.split("\t")])

		inputs = lineEntity[:self.inputLabelRatio[0]]
		labels = lineEntity[-self.inputLabelRatio[1]:]

		return (inputs, labels)
