"""
	Combines the network with a socketServer. Received data is evaluated in
	the network and emitted back via the socketServer
"""

import socketio
from flask import Flask
import eventlet

import numpy as np


class SensorCarController():
	"""
		Combines the network with the socketServer. Received data is evaluated
		in the network and emitted back via the socketServer
	"""

	network = None

	def __init__(self, network):
		"""
			Initiate sensorCarController with a instance of network which is
			used for evaluating sensorInformation
		"""

		self.network = network

		self.sio = socketio.Server()

		# Define events
		@self.sio.on('connect')
		def connect(sid, environ):
			print("Client connected: " + str(sid))

		@self.sio.on('disconnect')
		def disconnect(sid):
			print("Client disconnected: " + str(sid))

		@self.sio.on('evaluate')
		def evaluate(sid, data):
			print("Received package for evaluation")

			self.receive(data)

	def startServer(self):
		"""
			Starts the socketserver which listens for specific events
		"""

		wsgiApp = Flask(__name__)
		app = socketio.Middleware(self.sio, wsgiApp)

		try:
			eventlet.wsgi.server(eventlet.listen(("", 4567)), app)
			print("SocketServer started")

		except KeyboardInterrupt:
			print("SocketServer stopped")

	def receive(self, data):
		"""
			Called in the evaluate event. data is the JSON object received from
			the simulation. Has to be converted into an array and them evaluated
			in the net. In the end the evaluated data is emitted
		"""

		# Convert string of json to float list
		inputVector = np.array([float(data[key]) for key in data], dtype=np.float32)
		inputVector = np.array([3.952962, 36.34844, 17.27616], dtype=np.float32)

		# evaluate in net
		outputVector = self.network.evaluate(inputVector, normalize=True)[0][0]

		# todo make general

		# TODO recheck why list in list
		print(inputVector, "->", outputVector)

		# returne evaluated values to simulation
		self.sio.emit('steer', data={'steering_angle': str(outputVector)}, skip_sid=True)
