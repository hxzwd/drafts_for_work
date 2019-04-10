import os
import pickle
import copy
import numpy as np

from keras.models import model_from_json
from keras.models import load_model



def Doc(obj):
	print(obj.__doc__)

def tools_save_model(nn_model, return_file_names = False):
	model_name = nn_model.name
	default_nnet_dir = "nnets"
	filename_json = default_nnet_dir + "/" + model_name + ".json"
	filename_bin = default_nnet_dir + "/" + model_name + ".bin"

	nn_model_json = nn_model.to_json()
	
	handle = open(filename_json, "w")
	handle.write(nn_model_json)
	handle.close()

	nn_model_weights = nn_model.get_weights()
	handle = open(filename_bin, "wb")
	pickle.dump(nn_model_weights, handle)
	handle.close()

	if return_file_names:
		return filename_json, filename_bin
	return None

def tools_load_model(filename_json, filename_bin):
	
	handle = open(filename_json, "r")
	loaded_model_json = handle.read()
	handle.close()

	loaded_model = model_from_json(loaded_model_json)
	
	handle = open(filename_bin, "rb")
	loaded_model_weights = pickle.load(handle)
	handle.close()

	loaded_model.set_weights(loaded_model_weights)
	return loaded_model



#page_content = generate_gallery_html_page(20, 6, path_for_images = "imgs", target_file = "imgs/page.html", key_function = lambda x: int(x.split("_")[1]), gen_top_value = lambda x : x.split("_")[1], gen_bottom_value = lambda x: x.replace(".png", "").split("_")[3], row_headers = [ "header {}".format(i) for i in range(0, 6)], return_page_content = True)
#page_content = generate_gallery_html_page(20, 6, path_for_images = "imgs", target_file = "imgs/page.html", key_function = lambda x: int(x.split("_")[1]), gen_top_value = [ 0 for i in range(0, 120)], gen_bottom_value = [ "H" for i in range(0, 120) ], row_headers = [ "header {}".format(i) for i in range(0, 6)], return_page_content = True)
#page_content = generate_gallery_html_page(20, 6, path_for_images = "imgs", target_file = "imgs/page.html", key_function = lambda x: int(x.split("_")[1]), gen_top_value = [ 0 for i in range(0, 120)], gen_bottom_value = [ "i {}".format(i) for i in range(0, 120) ], row_headers = [ "header {}".format(i) for i in range(0, 6)], return_page_content = True, css_style_settings = ".bottom-left{left:-30px;}\n\t\t.column{padding:12px;}")
#page_content = generate_gallery_html_page(20, 6, path_for_images = "imgs", target_file = "imgs/page.html", key_function = lambda x: int(x.split("_")[1]), row_headers = lambda row : "index from {} to {}".format(*tuple((lambda x : [np.min(x), np.max(x)])(np.array(map(lambda x: map(int, x.replace(".png", "").split("_")[1::2]), row)).T[0]))))
#hf = lambda row : "index from {} to {}".format(*tuple((lambda x : [np.min(x), np.max(x)])(np.array(map(lambda x: map(int, x.replace(".png", "").split("_")[1::2]), row)).T[0])))

def update_css_object_settings(old_settings, new_settings):
	css_settings = copy.deepcopy(new_settings)
	css_settings = css_settings.items()
	for kk in old_settings.keys():
		if kk not in new_settings.keys():
			css_settings.append((kk, old_settings[kk]))
	return dict(css_settings)

def update_css_settings(old_settings, new_settings):
	css_settings = copy.deepcopy(new_settings)
	css_settings = css_settings.items()
	for kk in old_settings.keys():
		if kk not in new_settings.keys():
			css_settings.append((kk, old_settings[kk]))
		else:
			css_settings.append((kk, update_css_object_settings(old_settings[kk], new_settings[kk])))
	return dict(css_settings)
			

def get_new_css_data(css_data, css_style_settings):
	if css_style_settings == None:
		return css_data 
	if "str" in str(type(css_style_settings)):
		css_style_settings = [ i.strip().replace("}", "").split("{") for i in css_style_settings.strip().split("\n") ]
		css_style_settings = dict([ (i[0], dict(list(map(lambda x: tuple(map(lambda y : y.strip(), x.split(":"))), i[1].split(";")[0:-1])))) for i in css_style_settings ])
	css_data_list = [ i.strip().replace("}", "").split("{") for i in css_data.strip().split("\n") ]
	css_data_dict = dict([ (i[0], dict(list(map(lambda x: tuple(x.split(":")), i[1].split(";")[0:-1])))) for i in css_data_list ])
#	css_data_dict = dict([ tuple(i) for i in css_data_list ])
	new_css_data = "\n\t"
	css_new_settings = update_css_settings(css_data_dict, css_style_settings)
	for key, values in css_new_settings.items():
		new_css_object_data = "\t" + key + "{"
		new_css_object_data += "".join(i for i in [ "{}:{};".format(kk, vv) for kk, vv in values.items() ])
		new_css_object_data += "}\n\t"
		new_css_data += new_css_object_data
	return new_css_data

def generate_gallery_html_page(columns_num, rows_num, path_for_images = "", target_file = "images.html", key_function = None, gen_top_value = lambda x : "", gen_bottom_value = lambda x : "", row_headers = [], return_page_content = False, css_style_settings = None):
	css_data = "\n\t\t.column{float:left;width:auto;padding:12px;}\n\t\t.row::after{content:'';clear:both;display:table;}\n\t\t.container{position:relative;text-align:center;color:black;}\n\t\t.bottom-left{position:absolute;bottom:-4px;left:-20px;}\n\t\t.top-left{position:absolute;top:-4px;left:-20px;color:green;font-weight:bold;}\n\t"
	css_data = get_new_css_data(css_data, css_style_settings)
	html_body = "<body>\n<b>images:</b>\n<hr>"
	html_head = "<html>\n<head>\n\t<title>index.html</title>\n\t<style>{css_data}</style>\n</head>".format(css_data = css_data)
	html_begin = "{html_head}\n\n{html_body}\n\n".format(html_head = html_head, html_body = html_body)
	html_end = "\n\n</body>\n</html>"
	cell_template = "<div class=\"column\">\n\t<div class=\"container\">\n\t\t<img src=\"{image_source}\"/img>\n\t\t<div class=\"top-left\">{top_value}</div>\n\t\t<div class=\"bottom-left\">{bottom_value}</div>\n\t</div>\n</div>"
	row_template = "<div class=\"row\">\n\n{rows_cells}\n\n</div>"
	template_page = [ html_begin, html_end ]
	if path_for_images == "":
		path_for_images = os.getcwd()
	file_list = [ i for i in os.listdir(path_for_images) if ".png" in i ]
	total_size = rows_num * columns_num
	if key_function == None:
		pass
	else:
		file_list = sorted(file_list, key = key_function)
	if len(file_list) < total_size:
		file_list += [ None ] * (total_size - len(file_list))
	if len(file_list) > total_size:
		file_list = file_list[0:total_size]
	file_list = np.array(file_list)
	file_list = np.reshape(file_list, (rows_num, columns_num))
	if "function" in str(type(row_headers)):
		row_headers = list(map(row_headers, file_list))
	if row_headers == []:
		row_headers = [ "\n" ] * rows_num
	if len(row_headers) < rows_num:
		row_heades += [ "\n" ] * (rows_num - len(rows_headers))
	if len(row_headers) > rows_num:
		row_headers = row_headers[0:rows_num]
	if "list" in str(type(gen_top_value)):
		top_value_list = copy.deepcopy(gen_top_value)
		gen_top_value = lambda x : top_value_list[(np.reshape(file_list, (file_list.size,)).tolist()).index(x)]
	if "list" in str(type(gen_bottom_value)):
		bottom_value_list = copy.deepcopy(gen_bottom_value)
		gen_bottom_value = lambda x : bottom_value_list[(np.reshape(file_list, (file_list.size,)).tolist()).index(x)]
	html_data = ""
	for index, row in enumerate(file_list):
		row_string = row_template.format(rows_cells = "\n".join(i for i in list(map(lambda x: cell_template.format(image_source = x, top_value = gen_top_value(x), bottom_value = gen_bottom_value(x)), row))))
		html_data += row_headers[index] + "\n" + row_string + "\n"
	template_page.insert(1, html_data)
	page_content = "".join(i for i in template_page)
	handle = open(target_file, "w")
	handle.write(page_content)
	handle.close()
	if return_page_content:
		return page_content
	else:
		return None



