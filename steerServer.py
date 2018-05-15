import socketio
from flask import Flask
import eventlet


class SteerServer():

	def __init__(self):

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

	def receive(data):
		"""
			Data is the JSON object received from the simulation. Has to be
			converted into an array and them evaluated in the net
		"""
		
		# TODO convert to array

		# TODO evaluate in net

		data = {}

		# TODO returne evaluated values to simulation
		self.sio.emit('steer', data=data, skip_sid=True)
