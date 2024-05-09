from lxml.etree import ElementTree, TreeBuilder

from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtDisplay(QtWidget):
	def __init__(self, layout={}):
		super(QtDisplay, self).__init__("caFrame", name="content")
	
		self.form = QtWidget("QMainWindow", name="Form", layout=layout)
		self.widg = QtWidget("QWidget", name="centralwidget", layout={})
		
		self.form.append(self.widg, keep_original=True)
		self.widg.append(self, keep_original=True)	

		
	def updateProperties(self, macros={}):
		self.form.updateProperties(macros)
		
	def setProperty(self, key, prop):
		self.form.setProperty(key, prop)
		
		
	def writeQt(self, filename):		
		if "styleSheet" not in self.form:
			bg_col = Color(self.form.pop("background", "$BBBBBB"))
			stylesheet_str = "QWidget#centralwidget {background: rgba(" + str(bg_col["red"]) + "," + str(bg_col["green"]) + "," + str(bg_col["blue"]) + "," + str(bg_col["alpha"]) + ");}"
			stylesheet_str += "\nQPushButton::menu-indicator {image: url(none.png); width: 0}"
			self.form["styleSheet"] = String(stylesheet_str)
			
			
		self.form["windowTitle"] = String(self.form.pop("title", ""))
		
		margins = Rect(self.form.pop("margins", "0x0x0x0"))
		
		check_width = self["geometry"]["width"] + margins["x"] + margins["width"]
		check_height = self["geometry"]["height"] + margins["y"] + margins["height"]
		
		if check_width > self.form["geometry"]["width"]:
			self.form["geometry"]["width"] = check_width
		
		if check_height > self.form["geometry"]["height"]:
			self.form["geometry"]["height"] = check_height
		
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
