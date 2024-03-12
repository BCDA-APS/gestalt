from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from phoebusgen import screen

from gestalt.convert.phoebus.CSSWidget    import CSSWidget
from gestalt.convert.phoebus.CSSGroup     import CSSGroup
from gestalt.convert.phoebus.CSSDisplay   import CSSDisplay


class CSSGenerator(GestaltGenerator):
	def generateWidget(self, original, macros={}):
		return CSSWidget(original.classname, name=original.name, layout=original.attrs, macros=macros)
		
	def generateGroup(self, original, macros={}):
		return CSSGroup(name=original.name, layout=original.attrs, macros=macros)
		
	def generateAnonymousGroup(self, macros={}):
		return CSSGroup()
		
	def generateTextEntry(self, node, macros={}):
		return CSSWidget("TextEntry", name=node.name, layout=node.attrs, macros=macros)
		
	def generateMenu(self, node, macros={}):
		return CSSWidget("ComboBox", name=node.name, layout=node.attrs, macros=macros)
		
	def generateChoiceButton(self, node, macros={}):
		return CSSWidget("ChoiceButton", name=node.name, layout=node.attrs, macros=macros)
		
		
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
		
		
	def generateShellCommand(self, node, macros={}):
		output = CSSWidget("ActionButton", name=node.name, layout=node.attrs, macros=macros)
		
		for item in node.commands:
			_cmd = String(item.get("command", ""))
			_cmd.apply(macros)
			_cmd = _cmd.val
			
			_desc = String(item.get("label", ""))
			_desc.apply(macros)
			_desc = _desc.val
			
			output.widget.action_execute_command(_cmd, description=_desc)
				
		return output
		
		
	def generateMessageButton(self, node, macros={}):
		output = CSSWidget("ActionButton", name=node.name, layout=node.attrs, macros=macros)
		
		output.widget.action_write_pv(str(output.attrs.pop("pv")), str(output.attrs.pop("value")))
		
		return output
		
		
	def generateText(self, node, macros={}):
		output = CSSWidget("Label", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("border", "border-color")
		output.link("border_width", "border-width")
		
		output.attrs["transparent"] = Bool(False)
		
		return output
	
		
	def generateTextMonitor(self, node, macros={}):
		output = CSSWidget("TextUpdate", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("border", "border-color")	
		output.link("border_width", "border-width")
		
		return output

		
	def generateLED(self, node, macros={}):
		output = CSSWidget("LEDMultiState", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("line", "border-color")
		
		falseval = output.attrs.pop("false-value")
		trueval  = output.attrs.pop("true-value")
		
		falsecol = output.attrs.pop("false-color")
		truecol  = output.attrs.pop("true-color")
		undefcol = output.attrs.pop("undefined-color")
		
		output.widget.state(falseval.val, "", falsecol.val["red"], falsecol.val["green"], falsecol.val["blue"], falsecol.val["alpha"])
		output.widget.state(trueval.val, "", truecol.val["red"], truecol.val["green"], truecol.val["blue"], truecol.val["alpha"])
		
		output.widget.fallback_label("")
		output.widget.fallback_color(undefcol.val["red"], undefcol["green"], undefcol.val["blue"], undefcol.val["alpha"])
		
		return output

	
	def generateByteMonitor(self, node, macros={}):
		output = CSSWidget("ByteMonitor", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("on", "on-color")
		output.link("off", "off-color")
		output.link("startBit", "start-bit")
		output.link("numBits", "bits")
		
		output.attrs["square"] = Bool(True)
		
		return output
		
	
	def generateRectangle(self, node, macros={}):
		output = CSSWidget("Rectangle", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
			
		return output
		
		
	def generateEllipse(self, node, macros={}):
		output = CSSWidget("Ellipse", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
			
		return output
		
	
	def generateArc(self, node, macros={}):
		output = CSSWidget("Arc", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
		output.link("start_angle", "start-angle")
		output.link("total_angle", "span")
			
		return output
		
		
	def generatePolygon(self, node, macros={}):
		output = CSSWidget("Polygon", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
		
		for point in node.points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			output.widget.point(a_point["width"], a_point["height"])
		
		return output
		
		
	def generatePolyline(self, node, macros={}):
		output = CSSWidget("Polyline", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("line", "border-color")
		output.link("line_width", "border-width")
		
		for point in node.points:
			a_point = Rect(point)
			a_point.apply(macros)
			
			output.widget.point(a_point["width"], a_point["height"])
		
		return output
		
		
	def generateImage(self, node, macros={}):
		output = CSSWidget("Picture", name=node.name, layout=node.attrs, macros=macros)
		
		output.attrs["stretch_image"] = Bool(True)
		
		return output
		
		
	def generateSlider(self, node, macros={}):
		output = CSSWidget("Scrollbar", name=node.name, layout=node.attrs, macros=macros)
		
		return output

	
	def generateScale(self, node, macros={}):
		output = CSSWidget("Tank", name=node.name, layout=node.attrs, macros=macros)
		
		output.link("empty", "background")
		output.link("fill", "foreground")
		
		output.attrs["scale_visible"] = Bool(False)
		
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
