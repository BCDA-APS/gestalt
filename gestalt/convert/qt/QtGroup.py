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
		col = Color(self.pop("border-color")).val()
		wid = Number(self.pop("border-width")).val()
		
		if (int(wid) != 0) and (col["alpha"] != 0):
			border = QtWidget("QFrame")
			border["geometry"]["width"] = self["geometry"]["width"]
			border["geometry"]["height"] = self["geometry"]["height"]
		
			border["styleSheet"] = String(
"""\
QFrame
{{
    border-width: {width}px;
    border-style: solid;
    border-color: rgba({red},{green},{blue},{alpha});
}}
""".format(
			red=col["red"],
			green=col["green"],
			blue=col["blue"],
			alpha=col["alpha"],
			width=wid))

			self.children.insert(0, border)
		
		super(QtGroup, self).write(tree)
