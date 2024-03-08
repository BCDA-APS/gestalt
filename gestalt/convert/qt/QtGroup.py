from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtGroup(QtWidget):
	def __init__(self, name=None, layout={}, macros={}):
		super(QtGroup, self).__init__("caFrame", name=name, layout=layout)
	
		self.attrs["frameShape"] = Enum("QFrame::Box")
		self.attrs["backgroundMode"] = Enum("caFrame::Filled")
		
		self.attrs["background"] = Color(self.attrs.pop("background", "$00000000"))
		self.attrs["border-color"] = Color(self.attrs.pop("border-color", "$00000000"))
		self.attrs["border-width"] = Number(self.attrs.pop("border-width", 2))
	
	def write(self, tree):
		border = QtWidget("caGraphics")
		border.attrs["geometry"]["width"] = self["geometry"]["width"]
		border.attrs["geometry"]["height"] = self["geometry"]["height"]
		border.attrs["form"] = Enum("caGraphics::Rectangle")
		border.attrs["linestyle"] = Enum("Solid")
		border.attrs["fillstyle"] = Enum("Outline")		
		border.attrs["lineColor"] = Color(self.attrs.pop("border-color"))
		border.attrs["lineSize"] = Number(self.attrs.pop("border-width"))

		self.children.insert(0, border)
		
		super(QtGroup, self).write(tree)
