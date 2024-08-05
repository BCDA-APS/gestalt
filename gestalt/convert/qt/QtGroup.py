from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtGroup(QtWidget):
	def __init__(self, node=None, macros={}):
		super(QtGroup, self).__init__("caFrame", node=node, macros=macros)
	
		self["frameShape"] = Enum("QFrame::NoFrame")
		self["backgroundMode"] = Enum("caFrame::Filled")
		self["visibilityMode"] = Enum("caFrame::All")
		
		self.setDefault(Color, "background", "$00000000")
		self.setDefault(Color, "border-color", "$000000")
		self.setDefault(Number, "border-width", 0)
		self.setDefault(String, "border-style", "Solid")
		
	def write(self, tree):
		col = Color(self.pop("border-color")).val()
		wid = Number(self.pop("border-width")).val()
		style = String(self.pop("border-style")).val()
		
		if (int(wid) != 0) and (col["alpha"] != 0):
			border = QtWidget("QFrame")
			border["geometry"]["width"] = self["geometry"]["width"]
			border["geometry"]["height"] = self["geometry"]["height"]
		
			border["styleSheet"] = String(
"""\
QFrame
{{
    border-width: {width}px;
    border-style: {style};
    border-color: rgba({red},{green},{blue},{alpha});
}}
""".format(
			red=col["red"],
			green=col["green"],
			blue=col["blue"],
			alpha=col["alpha"],
			width=wid,
			style=style.lower()))

			self.children.insert(0, border)
		
		super(QtGroup, self).write(tree)
