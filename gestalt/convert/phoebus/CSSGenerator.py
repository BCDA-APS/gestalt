from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from phoebusgen import screen

from gestalt.convert.phoebus.CSSWidget    import CSSWidget
from gestalt.convert.phoebus.CSSDisplay   import CSSDisplay


class CSSGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return CSSWidget(original.classname, name=original.name, layout=original.attrs, macros=macros)
		
	def generateGroup(self, original, macros={}):
		output = CSSWidget("Group", name=original.name, layout=original.attrs, macros=macros)
	
		output.widget.transparent(True)
		output.widget.no_style()
	
		return output
		
	def generateAnonymousGroup(self, macros={}):
		output = CSSWidget("Group")
		
		output.widget.transparent(True)
		output.widget.no_style()
	
		return output
		
	def generateRelatedDisplay(self, node, macros={}):
		output = CSSWidget("ActionButton", name=node.name, layout=node.attrs, macros=macros)
		
		for item in node.links:
			_file = String(item.get("file", ""))
			_file.apply(macros)
			_file = _file.val
			
			_desc = String(item.get("label", ""))
			_desc.apply(macros)
			_desc = _desc.val
			
			_args = String(item.get("macros", ""))
			_args.apply(macros)
			_args = _args.val.split(",")
			
			_rep = "window"
			
			if "replace" in item and item.replace:
				_rep = "replace"
			
			_macros = {}
			
			for arg in _args:
				key, val = arg.split("=")
				_macros[key.strip()] = val.strip()
				
			output.widget.action_open_display(_file, _rep, description=_desc, macros=_macros)
				
		return output
		
	def generateMessageButton(self, node, macros={}):
		output = CSSWidget("ActionButton", name=node.name, layout=node.attrs, macros=macros)
		
		output.widget.action_write_pv(str(output.attrs.pop("pv")), str(output.attrs.pop("value")))
		
		return output
		
	def generateText(self, node, macros={}):
		output = CSSWidget("Label", name=node.name, layout=node.attrs, macros=macros)
		
		if "background" in output.attrs and "transparent" not in output.attrs:
			output.attrs["transparent"] = Bool("false")
		
		return output
		
	def generateTextEntry(self, node, macros={}):
		output = CSSWidget("TextEntry", name=node.name, layout=node.attrs, macros=macros)
		
		return output
		
	def generateTextMonitor(self, node, macros={}):
		output = CSSWidget("TextUpdate", name=node.name, layout=node.attrs, macros=macros)
		
		return output
		
	def generateMenu(self, node, macros={}):
		output = CSSWidget("ComboBox", name=node.name, layout=node.attrs, macros=macros)
		
		return output
		
	def generateChoiceButton(self, node, macros={}):
		output = CSSWidget("ChoiceButton", name=node.name, layout=node.attrs, macros=macros)
		
		if "horizontal" not in output.attrs:
			output.attrs["horizontal"] = Bool(False);
			
		if "selected" not in output.attrs and "background" in output.attrs:
			output.attrs["selected"] = output.attrs["background"]
		
		return output


def generateCSSFile(template, data, outputfile=""):
	a_display = CSSDisplay()
	the_generator = CSSGenerator()
	
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

						
	a_display.writeCSS(outputfile)
