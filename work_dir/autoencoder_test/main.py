
import os
import sys

import numpy as np

from prepare_data import get_mnist_data
from prepare_nn import create_dense_autoencoder
from misc_tools import tools_save_model, tools_load_model
from make_imgs import get_image_from_one_sample, get_images_from_dataset, del_all_images, make_html_page

	


(x_train, y_train), (x_test, y_test) = get_mnist_data()

filenames = [ "nnets/autoencoder.json", "nnets/autoencoder.bin" ]

autoencoder = tools_load_model(filenames[0], filenames[1])

encoder = autoencoder.get_layer("encoder")
decoder = autoencoder.get_layer("decoder")

autoencoder.compile(optimizer = "adam", loss = "binary_crossentropy")


part_size = 20
num_of_parts = 3
batch_size = part_size
row_heads = []

del_all_images()

for part_index in range(0, num_of_parts):
	x_test_part = x_test[0 + part_index * part_size : part_size * (part_index + 1) ]
	y_test_part = y_test[0 + part_index * part_size : part_size * (part_index + 1) ]

	encoded_imgs = encoder.predict(x_test_part, batch_size = batch_size)
	decoded_imgs = decoder.predict(encoded_imgs, batch_size = batch_size)

	get_images_from_dataset(x_test_part, y_test_part, save = True, length = None, start_index = 0 + ( part_index ) * part_size * 2)
	get_images_from_dataset(decoded_imgs, y_test_part, save = True, length = None, start_index = part_size + 2 * part_size * ( part_index ))

	images_interval = "(from {} to {})".format(part_index * part_size, (part_index + 1) * part_size)
	row_heads += "{original} {interval}\n{decoded} {interval}".format(decoded = "decoded images", original = "original images", interval = images_interval).split("\n")

html_data, html_content = make_html_page(row_len = part_size, return_html_data = True, row_heads = row_heads)

print(html_data)

sys.exit(0)

#
#encoder, decoder, autoencoder = create_dense_autoencoder()
#
#autoencoder.compile(optimizer = "adam", loss = "binary_crossentropy")
#
#epochs = 50
#batch_size = 256
#shuffle = True
#validation_data = (x_test, x_test)
#
#
#autoencoder.fit(x_train, x_train,
#		epochs = epochs,
#		batch_size = batch_size,
#		shuffle = shuffle,
#		validation_data = validation_data)
#

