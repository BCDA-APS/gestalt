from PyQt5.QtWidgets import *

class Input:
	def __init__(self, name, info):
		self.name = name
		self.description = info

templates = {}

def add(name, path='', qt_stylesheet=None, css_stylesheet=None, required_inputs=[], example=''):
	data = {}
	data["path"] = path[0]
	
	if qt_stylesheet:
		data["qt_stylesheet"] = path[0] + "/" + str(qt_stylesheet)
	
	if css_stylesheet:
		data["css_stylesheet"] = path[0] + "/" + str(css_stylesheet)
		
	data["thumbnail"] = path[0] + "/thumbnail.png"
	data["required_inputs"] = required_inputs
	data["example"] = example

	templates[name] = data
