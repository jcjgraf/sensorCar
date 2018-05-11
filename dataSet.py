"""

"""

import numpy as np
import linecache  # Get a specific line of a file


class DataSet():
	"""
		Manages dataSets
	"""

	def __init__(self, rawDataSetPath, inputLabelRatio):
		"""
			Initiate dataSet with a path to the rawDataSet and an array
			representing the ration between inputs and lables
		"""
		self.rawDataSetPath = rawDataSetPath

		self.processedDataSetPath = rawDataSetPath[:rawDataSetPath.rfind(".")] + ".scl"

		self.inputLabelRatio = inputLabelRatio

	def prepareDataSet(self):

		print("Preparing dataSet")

		# Scale DataSet
		# Open file and process it line by line
		with open(self.rawDataSetPath, "r") as f:

			print("Scaling database entries")

			for line in f:

				# An error is thrown when there is an empty line in the dataSet
				try:

					# split line entites into inputs and labels array
					lineEntities = np.array([float(i) for i in line.split("\t")])
					inputs = lineEntities[:self.inputLabelRatio[0]]
					labels = lineEntities[-self.inputLabelRatio[1]:]

					# Scale inputs/lables
					# divide 1 by the array, if it is a by zero division insert 0 for it
					scaledInputs = np.divide(1, inputs, out=np.zeros_like(inputs), where=inputs != 0)
					scaledLables = np.divide(1, labels, out=np.zeros_like(labels), where=labels != 0)

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

			print("Finished scaling entries")

		print("DataSet is ready")

		# TODO Shuffle DataSet

	def generateTrainingTestSets(self, trainingTestRatio):
		"""
			Devides the dataSet into a training and test set by the given
			trainingTestRatio which is an array of two elements
		"""

		print("Generating training and test dataSet")

		# Get the number of lines in the dataSet by iterating over it
		numberOfLines = 0
		with open(self.processedDataSetPath, "r") as f:
			for line in f:
				numberOfLines += 1

		self.trainingDataSetPath = self.processedDataSetPath[:self.processedDataSetPath.rfind(".")] + "_training.scl"
		self.testDataSetPath = self.processedDataSetPath[:self.processedDataSetPath.rfind(".")] + "_test.scl"

		print(self.trainingDataSetPath)
		print(self.testDataSetPath)

		# Get the number of elements for the training set
		ratioSum = float(trainingTestRatio[0] + trainingTestRatio[1])

		numberOfTraining = int(round(float(trainingTestRatio[0]) * numberOfLines / ratioSum))
		# Split the dataSet according to the calculated number per set
		with open(self.processedDataSetPath, "r") as f:

			for (i, line) in enumerate(f):
				if i < numberOfTraining:
					with open(self.trainingDataSetPath, "a") as tr:
						tr.write(line)

				if i >= numberOfTraining:
					with open(self.testDataSetPath, "a") as te:
						te.write(line)

			print("Created training and test dataSet")

	def getInputLableEntity(self, lineNumber):
		"""
			Loads a specific lineindex of the dataSet file and returns a tule containing an vector of inputs and an lable vector
		"""

		# Get line at specific index
		line = linecache.getline(self.processedDataSetPath, lineNumber)  # Returns "" in when the "index is out of range"
		linecache.clearcache()

		if line == "":  # When "index out pf range" an empty string is returned
			return False

		# Create arrays of the line entities
		lineEntities = np.array([float(i) for i in line.split("\t")])

		inputs = lineEntities[:self.inputLabelRatio[0]]
		labels = lineEntities[-self.inputLabelRatio[1]:]

		return (inputs, labels)
