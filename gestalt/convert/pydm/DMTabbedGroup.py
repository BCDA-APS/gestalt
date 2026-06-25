from gestalt.Type import *

from gestalt.convert.pydm.DMWidget import DMWidget
from gestalt.convert.StyleUtils import qss_tabbed_group


class DMTabbedGroup(DMWidget):
	def __init__(self, node=None, macros=None):
		if macros is None:
			macros = {}
		super(DMTabbedGroup, self).__init__("QTabWidget", node=node, macros=macros)
		
	def write(self, tree):
		self["styleSheet"] = String(qss_tabbed_group(self))
		self["currentIndex"] = Number(0)
		
		super(DMTabbedGroup, self).write(tree)
		
	def place(self, child, x=None, y=None, keep_original=False):
		intermediary = DMWidget("QWidget", name=child.name + "_tab")
		
		intermediary["title"] = String(child.name)
		#intermediary["Fill"] = String("True")
		
		intermediary.place(child, x, y, keep_original)
		super().place(intermediary)

		
		
		
		
		
		
		
		
		
		
		
		
		
