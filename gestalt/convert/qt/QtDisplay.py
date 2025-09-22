from lxml.etree import ElementTree, TreeBuilder

from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtDisplay(QtWidget):
	def __init__(self, layout={}):
		super(QtDisplay, self).__init__("caFrame", name="content", layout=layout)
		
	def writeQt(self, filename):	
		form = QtWidget("QMainWindow", name="Form", layout={})
		widg = QtWidget("QWidget", name="centralwidget", layout={})
		
		widg.append(self, keep_original=True)	
		form.append(widg, keep_original=True)

		form["geometry"] = self["geometry"]
		
		if "styleSheet" not in self:
			bg_col = Color(self.pop("background", "$BBBBBB"))
			stylesheet_str = "QWidget#centralwidget {background: rgba(" + str(bg_col["red"]) + "," + str(bg_col["green"]) + "," + str(bg_col["blue"]) + "," + str(bg_col["alpha"]) + ");}"
			stylesheet_str += "\nQPushButton::menu-indicator {image: url(none.png); width: 0}"
			form["styleSheet"] = String(stylesheet_str)
		else:
			form["styleSheet"] = self.pop("styleSheet")
			
			
		form["windowTitle"] = String(self.pop("title", ""))
		
		tree = TreeBuilder()
		
		tree.start("ui", {"version" : "4.0"})
		tree.start("class", {})
		tree.data("Form")
		tree.end("class")
		
		form.write(tree)
		
		tree.end("ui")
		
		writer = ElementTree(element=tree.close())
		writer.write(filename, pretty_print=True)
