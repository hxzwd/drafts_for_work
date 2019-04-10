
import os
import sys

import numpy as np

from prepare_data import get_mnist_data
from prepare_nn import create_dense_autoencoder
from misc_tools import tools_save_model, tools_load_model
from make_imgs import get_image_from_one_sample, get_images_from_dataset, del_all_images, make_html_page


def make_tests(autoencoder, dataset, params = None, return_result_dict = False):

	encoder = autoencoder.get_layer("encoder")
	decoder = autoencoder.get_layer("decoder")

	(x_train, y_train, x_test, y_test) = dataset

#	autoencoder.compile(optimizer = "adam", loss = "binary_crossentropy")	

	part_size = 20
	num_of_parts = 3
	batch_size = part_size
	row_heads = []

	return_dict = []


	if params != None:
		part_size = params["part_size"]
		num_of_parts = params["num_of_parts"]
		batch_size = params["batch_size"]

	return_dict += [ ("part_size", part_size), ("num_of_parts", num_of_parts), ("batch_size", batch_size) ]

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
		
		return_dict += [ ("x_test_part_{}".format(part_index) , x_test_part), ("y_test_part_{}".format(part_index), y_test_part) ]
		return_dict += [ ("encoded_imgs_{}".format(part_index) , encoded_imgs), ("decoded_imgs_{}".format(part_index), decoded_imgs) ]


	html_data, html_content = make_html_page(row_len = part_size, return_html_data = True, row_heads = row_heads)

	return_dict += [ ("html_content", html_content), ("html_data", html_data), ("row_heads", row_heads) ]

	if return_result_dict:
		return dict(return_dict)
	else:
		return None


