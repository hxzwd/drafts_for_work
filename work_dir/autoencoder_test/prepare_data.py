

from keras.datasets import mnist
import numpy as np


def get_mnist_data():
	(x_train, y_train), (x_test, y_test) = mnist.load_data()

	x_train = x_train.astype("float32")/255.0
	x_test = x_test.astype("float32")/255.0

	x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
	x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

	return (x_train, y_train), (x_test, y_test)
