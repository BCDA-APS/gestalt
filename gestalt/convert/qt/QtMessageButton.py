import pathlib

from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtMessageButton(QtWidget):
	def __init__(self, node=None, macros={}):		
		super(QtMessageButton, self).__init__("QFrame")

		self.button = QtWidget("caMessageButton", node=node, macros=macros)
		self["geometry"] = self.button.pop("geometry")
		
		self.button.link("label", "text")
		self.button.link("channel", "pv")
		self.button.link("pressMessage", "value")
			
		self.button["colorMode"] = Enum("caMessageButton::Static")
		self.button["fontScaleMode"] = Enum("EPushButton::None")
		
	def updateProperties(self, macros={}):
		super(QtMessageButton, self).updateProperties(macros)
		self.button.updateProperties(macros)
		
	def setProperty(self, key, prop):
		if key == "geometry":
			super(QtMessageButton, self).setProperty(key, prop)
		else:
			self.button.setProperty(key, prop)
		
	def write(self, tree):
		self.button["geometry"] = Rect((self["geometry"]["width"], self["geometry"]["height"]))
		self.button.position(x=0,y=0)
		
		the_font = self.button.pop("font")
		
		style = the_font["style"].lower()
		
		if "regular" in style:
			style = ""
		
		align = str(self.button.pop("alignment"))
		
		frame_align = "center"
		
		if "AlignLeft" in align:
			frame_align = "left"
		elif "AlignRight" in align:
			frame_align = "right"
			
		self.properties["attrs"]["styleSheet"] = String(
"""\
QPushButton
{{
    font-family: {family};
    font: {style} {size}px;
	
    text-align: {lcr};
}}
""".format(
	family = the_font["family"],
	style  = style,
	size   = the_font["size"],
	lcr    = frame_align))
	
		self.children.append(self.button)
		
		super(QtMessageButton, self).write(tree)
