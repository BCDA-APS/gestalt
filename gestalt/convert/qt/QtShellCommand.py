from gestalt.Type import *

from gestalt.convert.qt.QtWidget import QtWidget

class QtShellCommand(QtWidget):
	def __init__(self, node=None, macros={}):		
		super(QtShellCommand, self).__init__("QFrame")

		self.button = QtWidget("caShellCommand", node=node, macros=macros)
		self["geometry"] = self.button.pop("geometry")
		
		self.button["label"] = String("-" + str(self.button.pop("text")))
		
		labels = ""
		commands = ""
		args = ""
		
		for item in node.commands:
			labels += str(item.get("label", "")) + ";"
			commands  += str(item.get("command", "")) + ";"
			args   += ";"
			
			
		self.button["labels"] = String(labels.rstrip(";"))
		self.button["files"]  = String(commands.rstrip(";"))
		self.button["args"]   = String(args.rstrip(";"))
		
		
	def updateProperties(self, macros={}):
		super(QtShellCommand, self).updateProperties(macros)
		self.button.updateProperties(macros)
		
	def setProperty(self, key, prop):
		if key == "geometry":
			super(QtShellCommand, self).setProperty(key, prop)
		else:
			self.button.setProperty(key, prop)
			
	def write(self, tree):
		self.button["geometry"] = Rect((self["geometry"]["width"], self["geometry"]["height"]))
		self.button.position(x=0,y=0)
		
		the_font = self.button.pop("font")
		align = self.button.pop("alignment")
		
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
    font: {style} {size}pt;
	
    text-align: {lcr};
}}
""".format(
	family = the_font["family"],
	style  = the_font["style"].lower(),
	size   = the_font["size"],
	lcr    = frame_align))
	
		self.children.append(self.button)
		
		super(QtShellCommand, self).write(tree)
