from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget
from gestalt.convert.StyleUtils import qss_font

class QtRelatedDisplay(QtWidget):
	def __init__(self, node=None, macros=None):
		if macros is None: macros = {}
		super(QtRelatedDisplay, self).__init__("QFrame", loc=node.location)

		self.button = QtWidget("caRelatedDisplay", node=node, macros=macros)
		self["geometry"] = self.button.pop("geometry")

		labels = ""
		files = ""
		args = ""
		replace = ""

		for item in node["links"]:
			labels += item.get("label", "") + ";"
			files += item.get("file", "") + ".ui;"
			args += item.get("macros", "") + ";"

			if "replace" in item and item["replace"]:
				replace += "true;"
			else:
				replace += "false;"

		self.button["labels"] = String(labels.removesuffix(";"))
		self.button["files"]  = String(files.removesuffix(";"))
		self.button["args"]   = String(args.removesuffix(";"))
		self.button["removeParent"] = String(replace.removesuffix(";"))

		self.button["stackingMode"] = Enum("Menu")
		self.button["fontScaleMode"] = Enum("EPushButton::WidthAndHeight")

		self.tocopy.append("button")

	def setProperty(self, key, prop):
		if key == "geometry":
			super(QtRelatedDisplay, self).setProperty(key, prop)
		else:
			self.button.setProperty(key, prop)

	def write(self, tree):
		self.button["label"] = String("-" + str(self.button.pop("text")))

		self.button["geometry"] = Rect((self["geometry"]["width"], self["geometry"]["height"]))
		self.button.position(x=0,y=0)

		the_font = self.button.pop("font")
		self.button.pop("alignment")

		self.properties["attrs"]["styleSheet"] = String(qss_font("QPushButton", the_font))

		self.children.append(self.button)

		super(QtRelatedDisplay, self).write(tree)
