from gestalt.Type import *

from gestalt.convert.pydm.DMWidget import DMWidget
from gestalt.convert.pydm.StyleWriters import write_frameborder

def write_group(node):
	bg_col = Color(node.pop("background"))
	stylesheet_str = "QWidget {background: rgba(" + str(bg_col["red"]) + "," + str(bg_col["green"]) + "," + str(bg_col["blue"]) + "," + str(bg_col["alpha"]) + ");}"
	
	return stylesheet_str

class DMGroup(DMWidget):
	def __init__(self, node=None, macros={}):
		super(DMGroup, self).__init__("QFrame", node=node, macros=macros)
		
		#self["frameShape"] = Enum("QFrame::NoFrame")
		#self["backgroundMode"] = Enum("caFrame::Filled")
		#self["visibilityMode"] = Enum("caFrame::All")
		
		self.setDefault(Color, "background", "$00000000")
		self.setDefault(Color, "border-color", "$000000")
		self.setDefault(Number, "border-width", 0)
		self.setDefault(String, "border-style", "Solid")
		
		self.addStyleWriter(write_frameborder)
		self.addStyleWriter(write_group)
