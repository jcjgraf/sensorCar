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

				print("trainingDataSetPath and testDataSetPath exist, assigning them to attributes")

				self.trainingDataSetPath = trainingDataSetPath
				self.testDataSetPath = testDataSetPath

			# Generate them if they do not exists yet
			else:
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

		print("Splitting fullDataSetPath into trainingDataSetPath and testDataSetPath")

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

			print("Done creating training and test dataSet")
