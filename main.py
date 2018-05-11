#! /usr/bin/env python3

"""
	Main script of the sensorCar project
"""

from sensorCarController import SensorCarController


if __name__ == '__main__':

	path = "./simulation/dataSet/track636613955649037100.txt"

	sensorCar = SensorCarController([3, 10, 1], path, [3, 1])
	sensorCar.dataSet.prepareDataSet()
	sensorCar.dataSet.generateTrainingTestSets()

	print("DeltaError: {}".format(sensorCar.getPerformance()))

	sensorCar.trainNetwork()

	print("DeltaError: {}".format(sensorCar.getPerformance()))