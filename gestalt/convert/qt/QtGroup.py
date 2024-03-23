from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtGroup(QtWidget):
	def __init__(self, node=None, macros={}):
		super(QtGroup, self).__init__("caFrame", node=node, macros=macros)
	
		self["frameShape"] = Enum("QFrame::Box")
		self["backgroundMode"] = Enum("caFrame::Filled")
		
		self["background"] = Color(self.pop("background", "$00000000"))
		self["border-color"] = Color(self.pop("border-color", "$00000000"))
		self["border-width"] = Number(self.pop("border-width", 2))
	
	def write(self, tree):
		border = QtWidget("caGraphics")
		border["geometry"]["width"] = self["geometry"]["width"]
		border["geometry"]["height"] = self["geometry"]["height"]
		border["form"] = Enum("caGraphics::Rectangle")
		border["linestyle"] = Enum("Solid")
		border["fillstyle"] = Enum("Outline")		
		border["lineColor"] = Color(self.pop("border-color"))
		border["lineSize"] = Number(self.pop("border-width"))

		self.children.insert(0, border)
		
		super(QtGroup, self).write(tree)
