
import os
import sys

import numpy as np

from prepare_data import get_mnist_data
from prepare_nn import create_dense_autoencoder

from tests import make_tests	

python_command_make_test = "make_tests(autoencoder, (x_train, y_train, x_test, y_test))"


(x_train, y_train), (x_test, y_test) = get_mnist_data()

encoder, decoder, autoencoder = create_dense_autoencoder()

autoencoder.compile(optimizer = "adam", loss = "binary_crossentropy")

epochs = 1
batch_size = 256
shuffle = True
validation_data = (x_test, x_test)


learning_history = autoencoder.fit(x_train, x_train,
		epochs = epochs,
		batch_size = batch_size,
		shuffle = shuffle,
		validation_data = validation_data)

