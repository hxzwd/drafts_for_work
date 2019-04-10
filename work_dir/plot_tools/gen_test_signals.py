
import os
import sys
import pickle

import numpy as np

from matplotlib import pyplot as plt


load_signal_data = True
signal_bin_dump = "data/signals.bin"

def fill_string_index(index, size):
	if len(str(index)) == size:
		return str(index)
	if len(str(index)) > size:
		return None
	if len(str(index)) < size:
		return ("0" * (size - len(str(index)))) + str(index)

def plot_one_sample(x_data, y_data, target_path = "plots", name = "", plot_settings = ""):
	if name == "":
		name = "default"
	filename = "{}/{}.png".format(target_path, name)
	fig, ax = plt.subplots(1, 1)
	ax.grid(True)
	ax.plot(x_data, y_data)
	ax.set_title(name)
	ax.set_xlabel("x_data")
	ax.set_ylabel("y_data")
	fig.savefig(filename)
	fig.clf()
	fig.clear()
	del fig	

if load_signal_data:
	handle = open(signal_bin_dump, "rb")
	signal_info = pickle.load(handle)
	handle.close()
	num_of_signals = signal_info["num_of_signals"]
	max_signal_len = signal_info["max_signal_len"]
	min_signal_len =  signal_info["min_signal_len"]
	signal_params = signal_info["signal_params"]
	signal_data = signal_info["signal_data"]
else:
	num_of_signals = 20
	max_signal_len = 5000
	min_signal_len = 2000

	signal_params = []
	signal_params = np.random.randint(min_signal_len, high = max_signal_len, size = (num_of_signals, ))


	signal_data = [ sorted(np.random.random_sample((length, 2)).tolist(), key = lambda x : x[0]) for length in signal_params ]
	signal_data = [ np.array(i).T for i in signal_data ]


x_data = [ i[0] for i in signal_data ]
y_data = [ i[1] for i in signal_data ]


max_index = len(signal_data) - 1
max_index_len = len(str(max_index))

for index, signal in enumerate(signal_data):
	plot_one_sample(signal[0], signal[1], name = "plot_{}".format(fill_string_index(index, max_index_len)))

