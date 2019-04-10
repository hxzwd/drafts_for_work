
import os
import sys

import numpy as np

from PIL import Image

def get_image_from_one_sample(data, save = False, name = ""):
	image_size = (28, 28)
	byte_data = str(bytearray(np.reshape((data * 255.0).astype("uint8"), (28 * 28, ))))
	img = Image.frombytes("L", image_size, byte_data)
	if save:
		default_dir = "imgs"
		filename = default_dir + "/" + name + ".png"
		img.save(filename)
		return None
	return img


def get_images_from_dataset(x_dataset, y_dataset, save = False, length = None, start_index = 0):
	x_ds = x_dataset[0:length]
	y_ds = y_dataset[0:length]
	images_list = []
	for index, data in enumerate(x_ds):
		name = "sample_{}_digit_{}".format(index + start_index, y_ds[index])
		if save:
			get_image_from_one_sample(data, save = True, name = name)
		else:
			tmp_tuple = (name, get_image_from_one_sample(data, save = False, name = ""))
			images_list.append(tmp_tuple)
	if save:
		return None
	return dict(images_list)

def del_all_images(method = "system"):
	default_dir = "imgs"
	full_path = "/home/hjk/work_dir/autoencoder_test/{}".format(default_dir)
	cmd = "rm -f {}/*.png".format(full_path)
	if method == "popen":
		p = os.popen(cmd)
		output =  p.read()
		if output == "":
			return None
		else:
			return output
	else:
		os.system(cmd)
		return None


	
def make_html_page(row_len = 10, return_html_data = False, row_heads = []):
	row_len = row_len
	default_dir = "imgs"
	full_path = "/home/hjk/work_dir/autoencoder_test/{}".format(default_dir)
	filename = "index.html"
	file_list = sorted([ i for i in os.listdir(full_path) if ".png" in i ], key = lambda x: int(x.split("_")[1]))
	num_of_files = len(file_list)
	num_of_rows = (int)(np.ceil((float)(num_of_files)/row_len))
	if len(row_heads) < num_of_rows:
		row_heads = row_heads + [ "\n" ] * (num_of_rows - len(row_heads))
	if row_heads == []:
		row_heads = [ "\n" ] * num_of_rows
	css_data = "\n\t\t.column{float:left;width:auto;padding:12px;}\n\t\t.row::after{content:'';clear:both;display:table;}\n\t\t.container{position:relative;text-align:center;color:black;}\n\t\t.bottom-left{position:absolute;bottom:-4px;left:-10px;}\n\t\t.top-left{position:absolute;top:-4px;left:-20px;color:green;font-weight:bold;}\n\t"
	html_body = "<body>\n<b>images:</b>\n<hr>"
	html_head = "<html>\n<head>\n\t<title>index.html</title>\n\t<style>{css_data}</style>\n</head>".format(css_data = css_data)
	html_begin = "{html_head}\n\n{html_body}\n\n".format(html_head = html_head, html_body = html_body)
	html_end = "\n\n</body>\n</html>"
	cell_template = "\n<div class=\"column\">\n\t<div class=\"container\">\n\t\t<img src=\"{file}\"/img>\n\t\t<div class=\"top-left\">{index}</div>\n\t\t<div class=\"bottom-left\">{digit}</div>\n\t</div>\n</div>\n"
	row_template = "\n<div class=\"row\">\n{cells}\n</div>\n"
	html_content = ""
	html_data = ""
	row_data = ""
	counter = 0
	row_counter = 0
	for ii, i in enumerate(file_list):
		index, digit = i.replace(".png", "").split("_")[1::2]
		row_data = row_data + cell_template.format(file = i, index = index, digit = digit)
		if counter == row_len - 1 or ii == len(file_list) - 1:
			counter = 0
			html_content += row_heads[row_counter] + row_template.format(cells = row_data)
			row_data = ""
			row_counter += 1
			continue
		else:
			counter += 1
	html_data = html_begin + html_content + html_end
	handle = open("{}/{}".format(full_path, filename), "w")
	handle.write(html_data)
	handle.close()
	if return_html_data:
		return html_data, html_content
	else:
		return None

	

