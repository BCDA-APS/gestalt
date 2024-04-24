from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtLED(QtWidget):
	def __init__(self, node=None, macros={}):
		super(QtLED, self).__init__("caLed", node=node, macros=macros)
		
		self.link("channel", "pv")
		self.link("rectangular", "square")
		self.link("falseColor", "false-color")
		self.link("falseValue", "false-value")
		self.link("trueColor", "true-color")
		self.link("trueValue", "true-value")
		self.link("undefinedColor", "undefined-color")
		self.link("borderColor", "border-color")
	
		self["gradientEnabled"] = Bool(False)
		self["scaleContents"]   = Bool(True)
		
	def write(self, tree):
		self["ledWidth"] = self["geometry"]["width"]
		self["ledHeight"] = self["geometry"]["height"]
		
		super(QtLED, self).write(tree)
