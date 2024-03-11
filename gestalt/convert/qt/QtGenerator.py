from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from gestalt.convert.qt.QtWidget import QtWidget
from gestalt.convert.qt.QtGroup  import QtGroup
from gestalt.convert.qt.QtDisplay import QtDisplay


class QtGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return QtWidget(original.classname, name=original.name, layout=original.attrs, macros=macros)
		
	def generateGroup(self, original, macros={}):
		return QtGroup(name=original.name, layout=original.attrs, macros=macros)
	
	def generateAnonymousGroup(self, macros={}):
		return QtGroup()
		
	def generateRelatedDisplay(self, node, macros={}):
		output = QtWidget("caRelatedDisplay", name=node.name, layout=node.attrs, macros=macros)
		
		output.attrs["label"] = String("-" + str(output.attrs.pop("text")))
		
		labels = ""
		files = ""
		args = ""
		replace = ""
		
		for item in node.links:
			labels += str(item.get("label", "")) + ";"
			files  += str(item.get("file", "")) + ";"
			args   += str(item.get("macros", "")) + ";"
			
			if "replace" in item and item.replace:
				replace += "true;"
			else:
				replace += "false;"

		output.attrs["labels"] = String(labels.rstrip(";"))
		output.attrs["files"]  = String(files.rstrip(";"))
		output.attrs["args"]   = String(args.rstrip(";"))
		output.attrs["removeParent"] = String(replace.rstrip(";"))
		output.attrs["stackingMode"] = Enum("Menu")
		
		return output
		
		
	def generateMessageButton(self, node, macros={}):
		output = QtWidget("caMessageButton", name=node.name, layout=node.attrs, macros=macros)

		output.link("label", "text")
		output.link("channel", "pv")
		output.link("pressMessage", "value")
			
		output.attrs["colorMode"] = Enum("caMessageButton::Static")
			
		return output
		
		
	def generateText(self, node, macros={}):
		output = QtWidget("caLabel", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("borderColor", "border-color")
		output.link("borderWidth", "border-width")
		
		output.attrs["fontScaleMode"] = Enum("ESimpleLabel::None")
		
		return output
		
		
	def generateTextEntry(self, node, macros={}):
		output = QtWidget("caTextEntry", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
			
		output.attrs["colorMode"]     = Enum("caLineEdit::Static")
		output.attrs["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
		
	def generateTextMonitor(self, node, macros={}):
		output = QtWidget("caLineEdit", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("frameColor", "border-color")
		output.link("frameWidth", "border-width")
			
		output.attrs["colorMode"]     = Enum("caLineEdit::Static")
		output.attrs["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
		
	def generateMenu(self, node, macros={}):
		output = QtWidget("caMenu", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
			
		output.attrs["colorMode"] = Enum("caMenu::Static")
		
		return output
		
		
	def generateChoiceButton(self, node, macros={}):
		output = QtWidget("caChoice", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("bordercolor", "selected")
		
		if output.attrs.pop("horizontal"):
			output.attrs["stackingMode"] = Enum("Row")
			
		output.attrs["colorMode"] = Enum("caChoice::Static")
		
		return output
		
		
	def generateLED(self, node, macros={}):
		output = QtWidget("caLed", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("rectangular", "square")
		output.link("falseColor", "false-color")
		output.link("falseValue", "false-value")
		output.link("trueColor", "true-color")
		output.link("trueValue", "true-value")
		output.link("undefinedColor", "undefined-color")
		output.link("borderColor", "border-color")
	
		output.attrs["gradientEnabled"] = Bool(False)
		output.attrs["scaleContents"]   = Bool(True)
		
		return output
		
		
	def generateByteMonitor(self, node, macros={}):
		output = QtWidget("caByteController", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("channel", "pv")
		output.link("startBit", "start-bit")
		output.link("background", "off-color")
		output.link("foreground", "on-color")
		
		if output.attrs.pop("horizontal"):
			output.attrs["direction"] = Enum("caByte::Right")
		else:
			output.attrs["direction"] = Enum("caByte::Down")
			
		num_bits = output.attrs.pop("bits")
		
		output.attrs["endBit"] = Number(int(output.attrs["startBit"]) + int(num_bits) - 1)
		
		return output
		
		
	def generateRectangle(self, node, macros={}):
		output = QtWidget("caGraphics", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("foreground", "background")
		output.link("lineSize",   "border-width")
		output.link("lineColor",  "border-color")
		
		output.attrs["form"] = Enum("caGraphics::Rectangle")
		output.attrs["fillstyle"] = Enum("caGraphics::Filled")
		
		return output
		

def generateQtFile(template, data, outputfile=""):
	a_display = QtDisplay()
	the_generator = QtGenerator()
	
	for key, item in template.items():
		if isinstance(item, Node):
			if item.classname == "Form":
				a_display.setProperties(item.attrs)
			else:
				data.update({
					"__parentx__" : a_display["geometry"]["x"],
					"__parenty__" : a_display["geometry"]["y"],
					"__parentwidth__" : a_display["geometry"]["width"],
					"__parentheight__" : a_display["geometry"]["height"]})
			
				a_display.place(item.apply(the_generator, data=data))

						
	a_display.writeQt(outputfile)
