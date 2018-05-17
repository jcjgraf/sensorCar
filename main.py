#! /usr/bin/env python3

"""
	Main script of the sensorCar project
"""

from sensorCarController import SensorCarController
from steerServer import SteerServer


if __name__ == '__main__':

	path = "./simulation/dataSet/track636613955649037100.txt"

	sensorCarController = SensorCarController([3, 10, 1], path, [3, 1])

	# sensorCarController.dataSet.prepareDataSet()
	# sensorCarController.dataSet.generateTrainingTestSets()

	# print("DeltaError: {}".format(sensorCarController.getPerformance()))

	# sensorCarController.trainNetwork()

	# print("DeltaError: {}".format(sensorCarController.getPerformance()))

	sensorCarController.net.loadWeights("./weights/1805172358")

	ss = SteerServer(sensorCarController)
