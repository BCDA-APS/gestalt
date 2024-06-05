from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtGroup(QtWidget):
	def __init__(self, node=None, macros={}):
		super(QtGroup, self).__init__("caFrame", node=node, macros=macros)
	
		self["frameShape"] = Enum("QFrame::NoFrame")
		self["backgroundMode"] = Enum("caFrame::Filled")
		self["visibilityMode"] = Enum("caFrame::All")
		
		self["background"] = Color(self.pop("background", "$00000000"))
		self["border-width"] = Number(self.pop("border-width", 0))
		
		if int(self["border-width"]) == 0:
			self.pop("border-color")
			self["border-color"] = Color("$00000000")
		else:
			self["border-color"] = Color(self.pop("border-color", "$000000"))
		
	
	def write(self, tree):
		border = QtWidget("caGraphics")
		border["geometry"]["width"] = self["geometry"]["width"]
		border["geometry"]["height"] = self["geometry"]["height"]
		border["form"] = Enum("caGraphics::Rectangle")
		border["linestyle"] = Enum("Solid")
		border["fillstyle"] = Enum("Outline")
		border["lineColor"] = Color(self.pop("border-color"))
		border["lineSize"] = Number(self.pop("border-width"))
		
		if (int(border["lineSize"]) != 0 or border["lineColor"].val()["alpha"] != 0):
			self.children.insert(0, border)
		
		super(QtGroup, self).write(tree)
