"""
	DataSets is responsible for processing, normalising and providing dataSets
	entires to other classes for training of the network.
"""

import numpy as np
# import linecache  # Get a specific line of a file

import os.path  # check if a file exists at a certain path


class DataSet():
	"""
		DataSets is responsible for processing, normalising and providing
		dataSets entires to other classes for training of the network.
	"""

	fullDataSetPath = None
	trainingDataSetPath = None
	testDataSetPath = None

	def __init__(self, fullDataSetPath, inputLabelNumber, trainingTestRatio=[9, 1]):
		"""
			Initiate dataSet with a fullDataSetPath, inputLabelNumber an array
			representing the ration between inputs and lables. Optionally a
			trainingTestRatio array cen be given which determines the ration
			between training and test data. Default is 9:1
		"""

		self.inputLabelNumber = inputLabelNumber
		self.trainingTestRatio = trainingTestRatio

		# Check if path is valid and file exists
		if os.path.exists(fullDataSetPath):
			self.fullDataSetPath = fullDataSetPath

			# Check if the trainingDataSetPath and testDataSetPath file already exists
			trainingDataSetPath = self.fullDataSetPath[:self.fullDataSetPath.rfind(".")] + "_training.txt"
			testDataSetPath = self.fullDataSetPath[:self.fullDataSetPath.rfind(".")] + "_test.txt"

			# Assign them to attribute if they exists
			if os.path.exists(trainingDataSetPath) and os.path.exists(testDataSetPath):
				self.trainingDataSetPath = trainingDataSetPath
				self.testDataSetPath = testDataSetPath

			# Generate them if they do not exists yet
			if self.trainingDataSetPath is not None and self.testDataSetPath is not None:
				self.splitDataSet()

		else:
			print("Given path is invalid. Reasign right path to attribute")

	def normalizeInput(self, vector):
		"""
			Normalizes the vector by return a vector with the reciprocal value
			of each element in vector
		"""

		return np.divide(1, vector, out=np.zeros_like(vector), where=vector != 0)

	def splitDataSet(self):
		"""
			Split the fullDataSetPath by the trainingTestRation into two files,
			which are saved in the same path as the fullDataSetPath but with the
			ending "_training.txt" resp. "_test.txt".
		"""

		# Get number of lines(=data) in the fullDataSetPath
		numberOfLines = 0

		with open(self.fullDataSetPath, "r") as ff:
			for line in ff:
				numberOfLines += 1

		self.trainingDataSetPath = self.fullDataSetPath[:self.fullDataSetPath.rfind(".")] + "_training.txt"
		self.testDataSetPath = self.fullDataSetPath[:self.fullDataSetPath.rfind(".")] + "_test.txt"

		# Get the number of elements for the training set (testset equals the remainder)
		splitRatioSum = float(self.trainingTestRatio[0] + self.trainingTestRatio[1])
		numberTrainingEntities = int(round(float(self.trainingTestRatio[0]) * numberOfLines / splitRatioSum))

		# Split the entites of the fullDataSetPath into the two files
		with open(self.fullDataSetPath, "r") as ff:

			for (i, line) in enumerate(ff):
				if i < numberTrainingEntities:
					with open(self.trainingDataSetPath, "a") as trf:
						trf.write(line)

				if i >= numberTrainingEntities:
					with open(self.testDataSetPath, "a") as tef:
						tef.write(line)

			print("Created training and test dataSet")

	# def getInputLableEntities(self, lineNumber):
	# 	"""
	# 		Loads the line at lineNumber of the dataSet file and returns a tule
	# 		containing an vector of inputs and an lable vector if
	# 		trainingDataSetPath exists.
	# 		False is returned when the lineNumber is "out of range" or
	# 		trainingDataSetPath does not exist.
	# 	"""

	# 	if self.trainingDataSetPath is None:
	# 		print("trainingDataSet does not exist. Not possible to retrieve entities")
	# 		return False

	# 	# Get line at specific index
	# 	line = linecache.getline(self.trainingDataSetPath, lineNumber)  # Returns "" in when the "index is out of range"
	# 	linecache.clearcache()

	# 	if line == "":  # When "index out pf range" an empty string is returned
	# 		return False

	# 	# Create arrays of the line entities. Convert str to float
	# 	lineEntity = np.array([float(i) for i in line.split("\t")])

	# 	inputs = lineEntity[:self.inputLabelNumber[0]]
	# 	labels = lineEntity[-self.inputLabelNumber[1]:]

	# 	return (inputs, labels)
