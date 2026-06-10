from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtMessageButton(QtWidget):
	def __init__(self, node=None, macros=None):
		if macros is None: macros = {}
		super(QtMessageButton, self).__init__("QFrame", loc=node.location)

		self.button = QtWidget("caMessageButton", node=node, macros=macros)
		self["geometry"] = self.button.pop("geometry")

		self.button.link("label", "text")
		self.button.link("channel", "pv")
		self.button.link("pressMessage", "value")

		self.button["colorMode"] = Enum("caMessageButton::Static")
		self.button["fontScaleMode"] = Enum("EPushButton::Height")

		self.tocopy.append("button")

	def setProperty(self, key, prop):
		if key == "geometry":
			super(QtMessageButton, self).setProperty(key, prop)
		else:
			self.button.setProperty(key, prop)

	def write(self, tree):
		self.button["geometry"] = Rect((self["geometry"]["width"], self["geometry"]["height"]))
		self.button.position(x=0,y=0)

		the_font = self.button.pop("font")
		self.button.pop("alignment")

		style = the_font["style"].lower()

		if "regular" in style:
			style = ""

		self.properties["attrs"]["styleSheet"] = String(
"""\
QPushButton
{{
    font-family: {family};
    font: {style};
}}
""".format(
	family = the_font["family"],
	style  = style))

		self.children.append(self.button)

		super(QtMessageButton, self).write(tree)
