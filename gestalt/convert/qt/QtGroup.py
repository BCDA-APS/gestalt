from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtGroup(QtWidget):
	def __init__(self, name=None, layout={}, macros={}):
		super(QtGroup, self).__init__("caFrame", name=name, layout=layout)
	
		self.attrs["frameShape"] = Enum("QFrame::Box")
	
	def write(self, tree):
		background = QtWidget("caGraphics")
		background.attrs["geometry"]["width"] = self["geometry"]["width"]
		background.attrs["geometry"]["height"] = self["geometry"]["height"]
		background.attrs["form"] = Enum("caGraphics::Rectangle")
		background.attrs["linestyle"] = Enum("Solid")
		background.attrs["fillstyle"] = Enum("Filled")
		
		background.attrs["foreground"] = Color("$00000000")
		background.attrs["lineColor"] = Color("$00000000")
		
		if "background" in self.attrs:
			background.attrs["foreground"] = Color(self.attrs.pop("background"))
			background.attrs["lineColor"] = background.attrs["foreground"]

		self.attrs["background"] = Color(self.attrs.pop("border-color", Color("$00000000")))
			
		if "border-width" in self.attrs:
			self.attrs["lineWidth"] = Number(self.attrs.pop("border-width"))

		self.children.insert(0, background)
		
		super(QtGroup, self).write(tree)
