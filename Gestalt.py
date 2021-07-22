from lxml.etree import ElementTree, TreeBuilder

from gestalt.Type import *

import stylesheet
import yaml

name_numbering = {}


class Widget(object):
	def __init__(self, classname, name=None, layout=None):
		self.classname = classname
		
		if name:
			self.name = name
		else:
			num = name_numbering.get(classname, 0)
			num += 1
			name_numbering[classname] = num
			
			self.name = classname + str(num)
			
		self.attrs = {}
		self.children = []
		
		if layout:
			self.setProperties(layout)
			
	def position(self, *args, x=None, y=None):
			
		out_x = 0
		out_y = 0
			
		if len(args) == 2:
			out_x = args[0]
			out_y = args[1]
			
		elif not x is None:
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
			
			
		if self.attrs.get(key):
			self.attrs[key] = self.attrs[key].merge(to_assign)
		else:
			self.attrs[key] = to_assign

		return self

		
	def setProperties(self, layout):
		if not layout:
			return self
		
		for key, val in layout.items():
			self.setProperty(key, val)
			
		return self
		
		
	def addChild(self, child):
		self.children.append(child)
		return self
	
	def write(self, tree):
		tree.start("widget", {"class" : self.classname, "name" : self.name})
		
		for key, item in self.attrs.items():
			tree.start("property", {"name" : key})
			item.write(tree)
			tree.end("property")
						
		for child in self.children:
			child.write(tree)
			
		tree.end("widget")
		

class Display(Widget):
	def __init__(self, layout=None):
		super(Display, self).__init__("QWidget", name="centralwidget")
		
		self.form = Widget("QWidget", name="Form", layout=layout)
	
		self.form.addChild(self)
		
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
		
		self.form.write(tree)
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)
