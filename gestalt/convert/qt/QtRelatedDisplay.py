import pathlib

from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtRelatedDisplay(QtWidget):
	def __init__(self, node=None, macros={}):		
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


	def updateProperties(self, macros={}):
		super(QtRelatedDisplay, self).updateProperties(macros)
		self.button.updateProperties(macros)
		self.links.apply(macros)
		
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
		align = str(self.button.pop("alignment"))
		
		style = the_font["style"].lower()
		
		if "regular" in style:
			style = ""
		
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
    font: {style};
	
    text-align: {lcr};
}}
""".format(
	family = the_font["family"],
	style  = style,
	size   = the_font["size"],
	lcr    = frame_align))
	
		self.children.append(self.button)
		
		super(QtRelatedDisplay, self).write(tree)
