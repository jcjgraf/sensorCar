"""

"""

import socketio
from flask import Flask
import eventlet
import numpy as np


class SteerServer():
	"""

	"""

	def __init__(self, sensorCarController):
		"""
			Initialise steerServer with a sensorCarController which provides the
			ability to evaluate a inputvector in the net with a provided method.
		"""

		self.sensorCarController = sensorCarController

		self.sio = socketio.Server()
		wsgiApp = Flask(__name__)

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

		app = socketio.Middleware(self.sio, wsgiApp)

		try:
			eventlet.wsgi.server(eventlet.listen(("", 4567)), app)
		except KeyboardInterrupt	:
			print("Stopping SocketServer")

	def receive(self, data):
		"""
			Data is the JSON object received from the simulation. Has to be
			converted into an array and them evaluated in the net
		"""

		# Convert string of json to float list
		inputVector = np.array([float(data[key]) for key in data], dtype=float)

		# evaluate in net
		outputVector = self.sensorCarController.evaluate(inputVector)

		# todo make general

		# TODO recheck why list in list
		print("eval", outputVector[0][0])

		# returne evaluated values to simulation
		self.sio.emit('steer', data={'steering_angle': str(outputVector[0][0])}, skip_sid=True)
