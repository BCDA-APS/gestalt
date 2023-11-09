from lxml.etree import ElementTree, TreeBuilder

from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtDisplay(QtWidget):
	def __init__(self, layout=None):
		super(QtDisplay, self).__init__("QWidget", name="centralwidget")
	
		self.form = QtWidget("QWidget", name="Form", layout=layout)
	
		self.form.append(self, keep_original=True)
	
		
	def setProperties(self, layout):
		self.form.setProperties(layout)
		
	def setProperty(self, key, prop):
		self.form.setProperty(key, prop)
		
		
	def writeQt(self, filename):
		margins = Rect(x=0, y=0, width=0, height=0)
		margins = margins.merge(self.form.attrs.pop("margins", Rect(x=0, y=0, width=0, height=0)))
		
		self.form["geometry"]["width"]  = self["geometry"]["width"] + margins["x"] + margins["width"]
		self.form["geometry"]["height"] = self["geometry"]["height"] + margins["y"] + margins["height"]
		
		self["geometry"]["x"] = margins["x"]
		self["geometry"]["y"] = margins["y"]
		
		tree = TreeBuilder()
		
		tree.start("ui", {"version" : "4.0"})
		tree.start("class", {})
		tree.data("Form")
		tree.end("class")
		
		self.form.write(tree)
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)