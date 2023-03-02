from lxml.etree import ElementTree, TreeBuilder

from gestalt.Type import *

import copy
import yaml

name_numbering = {}


class Node(object):
	def __init__(self, classname, initial=None, layout=None):
		self.classname = classname
		self.name = None
		
		self.attrs = {}
		self.children = []
		
		if name is not None:
			self.name = name
		
		if layout is not None:
			self.setProperties(layout)
			
		if initial is not None:
			if isinstance(initial, dict):
				for childname, child in initial.items():
					child.name = childname
					self.addChild(child)
				
			elif isinstance(initial, list) or isinstance(initial, tuple):
				for child in initial:
					self.addChild(child)
					
					
	def setProperty(self, key, data):
		to_assign = None
		
		if isinstance(data, DataType):
			to_assign = data
		elif isinstance(data, bool):
			to_assign = Bool(data)
		elif isinstance(data, int):
			to_assign = Number(data)
		elif isinstance(data, float):
			to_assign = Double(data)
		elif isinstance(data, dict):
			to_assign = DataType(data)
		elif isinstance(data, str):
			to_assign = yaml.safe_load(data)
			
			if not isinstance(to_assign, DataType):
				to_assign = String(data)
			
			
		if key in self.attrs:
			self.attrs[key] = self.attrs[key].merge(to_assign)
		else:
			self.attrs[key] = to_assign

		return self
		
		
	def getProperty(self, key):
		return self.attrs[key]
					
	def __setitem__(self, key, data):
		self.setProperty(key, data)			
					
	def __getitem__(self, key):
		return self.getProperty(key)

		
	def append(self, child, keep_original=False):
		if not keep_original:
			cpy = copy.deepcopy(child)
		
			self.children.append(cpy)
			
		else:
			self.children.append(child)
			
		return self
		

	def generateQt (self, data={}):
		
		
		
		output = QtWidget(self.classname, name=self.name, layout=self.attrs
		
		


class QtWidget(object):
	def __init__(self, classname, initial=None, name=None, layout=None, macros={}):
		self.classname = classname
		self.macros = macros
		
		if name is not None:
			self.name = name
		else:
			num = 1 + name_numbering.get(classname, 0)
			name_numbering[classname] = num
			
			self.name = classname + str(num)
			
		self.attrs = {}
		self.children = []
		
		if layout is not None:
			self.setProperties(layout)
			
		if initial is not None:			
			if isinstance(initial, dict):
				for name, child in initial.items():
					child.name = name
					self.addChild(child)
			
			elif isinstance(initial, list) or isinstance(initial, tuple):
				for child in initial:
					self.addChild(child)
					
					
			
	def position(self, *args, x=None, y=None):
			
		out_x = 0
		out_y = 0
			
		if len(args) == 2:
			out_x = args[0]
			out_y = args[1]
			
		elif x is not None:
			out_x = x
			out_y = y
			
		elif len(args) == 1:
			if instanceof(args[0], list) or instanceof(args[0], tuple):
				out_x = args[0][0]
				out_y = args[0][1]
			elif instanceof(args[0], dict):
				out_x = args[0]["x"]
				out_y = args[0]["y"]				
		
		self.setProperty("geometry", Rect(x = out_x, y = out_y))
				
		return self
				
			
	def setProperty(self, key, data):
		to_assign = None
		
		if isinstance(data, DataType):
			to_assign = data
		elif isinstance(data, bool):
			to_assign = Bool(data)
		elif isinstance(data, int):
			to_assign = Number(data)
		elif isinstance(data, float):
			to_assign = Double(data)
		elif isinstance(data, dict):
			to_assign = DataType(data)
		elif isinstance(data, str):
			to_assign = yaml.safe_load(data)
			
			if not isinstance(to_assign, DataType):
				to_assign = String(data)
			
			
		if key in self.attrs:
			self.attrs[key] = self.attrs[key].merge(to_assign)
		else:
			self.attrs[key] = to_assign

		return self
		
	def getProperty(self, key):
		return self.attrs[key]

		
	def __setitem__(self, key, data):
		return self.setProperty(key, data)
		
	def __getitem__(self, key):
		return self.getProperty(key)
		
		
	def setProperties(self, *args, **kwargs):
		if len(args) != 0:
			for key, val in args[0].items():
				self.setProperty(key, val)
			
		if kwargs:
			for key, val in kwargs.items():
				self.setProperty(key, val)
			
		return self
		
		
	def addChild(self, child, macros={}, keep_original=False):
		if not keep_original:
			cpy = copy.deepcopy(child)
		
			cpy.macros.update(macros)
		
			self.children.append(cpy)
			
		else:
			child.macros.update(macros)
			self.children.append(child)
			
		return self
	
	def write(self, tree, in_macros):
		tree.start("widget", {"class" : self.classname, "name" : self.name})
		
		out_macros = {}
		out_macros.update(in_macros)
		out_macros.update(self.macros)
		
		for key, item in self.attrs.items():
			tree.start("property", {"name" : key})
			item.write(tree, out_macros)
			tree.end("property")
						
		for child in self.children:
			child.write(tree, out_macros)
			
		tree.end("widget")

		

class Display(Widget):
	def __init__(self, layout=None):
		super(Display, self).__init__("QWidget", name="centralwidget")
		
		self.form = Widget("QWidget", name="Form", layout=layout)
	
		self.form.addChild(self, keep_original=True)
		
	def setProperties(self, layout):
		self.form.setProperties(layout)
		
	def setProperty(self, key, prop):
		self.form.setProperty(key, prop)
		
		
	def writeQt(self, filename):
		tree = TreeBuilder()
		
		tree.start("ui", {"version" : "4.0"})
		tree.start("class", {})
		tree.data("Form")
		tree.end("class")
		
		self.form.write(tree, {})
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)
