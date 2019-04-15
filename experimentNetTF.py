import tensorflow as tf
import numpy as np
import os
import shutil

from functools import wraps

def callOnce(inputFunc):
	attribute = "_cache_" + inputFunc.__name__

	@property
	@wraps(inputFunc)
	def checkAttribute(self):
		if not hasattr(self, attribute):
			setattr(self, attribute, inputFunc(self))
		return getattr(self, attribute)

	return checkAttribute


class ExperimentNetTF:

	def __init__(self, shape, learningRate):
		self.shape = shape
		self.x = tf.placeholder(tf.float32, shape=[None, self.shape[0]], name="InputData")
		self.y = tf.placeholder(tf.float32, shape=[None, self.shape[-1]], name="LabelData")

		self.weights = self._getInitWeights()

		self.logDir = "./log/experiment"
		shutil.rmtree(self.logDir)
		os.makedirs(self.logDir)



		self.learningRate = learningRate

		self.summaryWriter = tf.summary.FileWriter(self.logDir, graph=tf.get_default_graph())

		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())

		self.output
		self.optimizer
		self.loss

		tf.summary.scalar("loss", self.loss)
		self.mergedSummary = tf.summary.merge_all()

	def _getInitWeights(self):
		return [tf.Variable(tf.truncated_normal([fromLayer, toLayer], stddev=0.1, name="Weight{}".format(i))) for i, (fromLayer, toLayer) in enumerate(zip(self.shape[:-1], self.shape[1:]))]

	def train(self, datasetPath, epochs=1):

		costMeanList = []

		for epoch in range(epochs):
			print(f"Epoch {epoch + 1}")
			with open(datasetPath, "r") as ds:

				costList = []

				for i, line in enumerate(ds):
					lineEntities = np.array([float(i) for i in line.split(",")], dtype=np.float128)

					inputs = np.reshape(lineEntities[:3], (1, 3))
					labels = np.reshape(np.divide(lineEntities[3:], 25), (1, 1))

					# inputs = np.reshape(lineEntities[:2], (1, 2))
					# labels = np.reshape(lineEntities[2:], (1, 1))

					_, loss, summary = self.sess.run([self.optimizer, self.loss, self.mergedSummary], {self.x: inputs, self.y: labels})

					costList.append(loss)
					self.summaryWriter.add_summary(summary, epoch * 1000 + epoch + i)

				tempList = np.array(costList)
				costMeanList.append(np.mean(tempList))

				addListSummary = tf.Summary()
				addListSummary.value.add(tag="MeanLoss", simple_value=np.mean(tempList))
				self.summaryWriter.add_summary(addListSummary, epoch)
				self.summaryWriter.flush()

		self.saveTrainingData("./experimentSave/test.txt", costMeanList)


	def getPrediction(self, xData):
		return self.sess.run(self.output, {self.x: xData})

	@callOnce
	def output(self):
		layerInput = self.x

		for weight in self.weights:
			layerInput = tf.math.tanh(tf.matmul(layerInput, weight))

		return layerInput

	@callOnce
	def loss(self):
		return tf.reduce_mean(tf.square(self.y - self.output))
		# return tf.square(self.y - self.output)

	@callOnce
	def optimizer(self):
		return tf.train.GradientDescentOptimizer(self.learningRate).minimize(self.loss)

	def saveTrainingData(self, filePath, lossList):

		file = open(filePath, "a")

		for loss in lossList:

			file.write(str(loss) + "\n")

		file.close()

	def doSave(self, step):
		savePath = self.saver.save(self.sess, os.path.join(self.savePath, "model"), global_step = step)
		print("Saved current model to {}".format(savePath))


if __name__ == '__main__':
	net = ExperimentNetTF([3, 10, 1], learningRate=0.0005)

	net.train("simulation/dataset/trackMaster1k.txt", epochs=10)

	# net.train("simulation/dataset/testAnd.txt", epochs=100)