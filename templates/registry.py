from PyQt5.QtWidgets import *

class Input:
	def __init__(self, name, info):
		self.name = name
		self.description = info

templates = {}

def add(name, path='', required_inputs=[], example=''):
	data = {}
	data["path"] = path[0]
	data["stylesheet"] = path[0] + "/layout.yml"
	data["thumbnail"] = path[0] + "/thumbnail.png"
	data["required_inputs"] = required_inputs
	data["example"] = example

	templates[name] = data
