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
		
		if "text" in output.attrs:
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
		
		if "text" in output.attrs:
			output.attrs["label"] = String(output.attrs.pop("text"))
			
		if "pv" in output.attrs:
			output.attrs["channel"] = String(output.attrs.pop("pv"))
			
		if "value" in output.attrs:
			output.attrs["pressMessage"] = String(output.attrs.pop("value"))
			
		output.attrs["colorMode"] = Enum("caMessageButton::Static")
			
		return output
		
	def generateText(self, node, macros={}):
		output = QtWidget("caLabel", name=node.name, layout=node.attrs, macros=macros)
		
		if "border-color" in output.attrs:
			output.attrs["borderColor"] = Color(output.attrs.pop("border-color"))
		
		if "border-width" in output.attrs:
			output.attrs["borderWidth"] = Number(output.attrs.pop("border-width"))
		
		output.attrs["fontScaleMode"] = Enum("ESimpleLabel::None")
		
		return output
		
	def generateTextEntry(self, node, macros={}):
		output = QtWidget("caTextEntry", name=node.name, layout=node.attrs, macros=macros)
		
		if "pv" in output.attrs:
			output.attrs["channel"] = String(output.attrs.pop("pv"))
			
		output.attrs["colorMode"] = Enum("caLineEdit::Static")
		output.attrs["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
	def generateTextMonitor(self, node, macros={}):
		output = QtWidget("caLineEdit", name=node.name, layout=node.attrs, macros=macros)
		
		if "pv" in output.attrs:
			output.attrs["channel"] = String(output.attrs.pop("pv"))
			
		if "border-color" in output.attrs:
			output.attrs["frameColor"] = Color(output.attrs.pop("border-color"))
		
		if "border-width" in output.attrs:
			output.attrs["frameWidth"] = Number(output.attrs.pop("border-width"))
			
		output.attrs["colorMode"] = Enum("caLineEdit::Static")
		output.attrs["fontScaleMode"] = Enum("caLineEdit::None")
		
		return output
		
	def generateMenu(self, node, macros={}):
		output = QtWidget("caMenu", name=node.name, layout=node.attrs, macros=macros)
		
		if "pv" in output.attrs:
			output.attrs["channel"] = String(output.attrs.pop("pv"))
			
		output.attrs["colorMode"] = Enum("caMenu::Static")
		
		return output
		
	def generateChoiceButton(self, node, macros={}):
		output = QtWidget("caChoice", name=node.name, layout=node.attrs, macros=macros)
		
		if "pv" in output.attrs:
			output.attrs["channel"] = String(output.attrs.pop("pv"))
			
		if "horizontal" in output.attrs and output.attrs["horizontal"]:
			output.attrs.pop("horizontal")
			output.attrs["stackingMode"] = Enum("Row")
			
		if "selected" in output.attrs:
			output.attrs["bordercolor"] = output.attrs.pop("selected")
			
		output.attrs["colorMode"] = Enum("caChoice::Static")
		
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
