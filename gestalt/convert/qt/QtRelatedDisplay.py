import pathlib

from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtRelatedDisplay(QtWidget):
	def __init__(self, node=None, macros={}):		
		super(QtRelatedDisplay, self).__init__("QFrame")

		self.button = QtWidget("caRelatedDisplay", node=node, macros=macros)
		self["geometry"] = self.button.pop("geometry")
		
		self.button["label"] = String("-" + str(self.button.pop("text")))
		
		labels = ""
		files = ""
		args = ""
		replace = ""
		
		for item in node.links:
			a_label = String(item.get("label", ""))
			a_label.apply(macros)

			a_file = String(item.get("file", ""))
			a_file.apply(macros)
			a_file = str(a_file).removesuffix( pathlib.PurePath(str(a_file)).suffix ) + ".ui"

			
			a_macro = String(item.get("macros", ""))
			a_macro.apply(macros)
			
			
			labels += str(a_label) + ";"
			files  += str(a_file) + ";"
			args   += str(a_macro) + ";"
			
			if "replace" in item and item.replace:
				replace += "true;"
			else:
				replace += "false;"

		self.button["labels"] = String(labels.rstrip(";"))
		self.button["files"]  = String(files.rstrip(";"))
		self.button["args"]   = String(args.rstrip(";"))
		self.button["removeParent"] = String(replace.rstrip(";"))
		self.button["stackingMode"] = Enum("Menu")
		
		
	def updateProperties(self, macros={}):
		super(QtRelatedDisplay, self).updateProperties(macros)
		self.button.updateProperties(macros)
		
	def setProperty(self, key, prop):
		if key == "geometry":
			super(QtRelatedDisplay, self).setProperty(key, prop)
		else:
			self.button.setProperty(key, prop)
		
	def write(self, tree):
		self.button["geometry"] = Rect((self["geometry"]["width"], self["geometry"]["height"]))
		self.button.position(x=0,y=0)
		
		the_font = self.button.pop("font")
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
	style  = the_font["style"].lower(),
	size   = the_font["size"],
	lcr    = frame_align))
	
		self.children.append(self.button)
		
		super(QtRelatedDisplay, self).write(tree)
