from gestalt.Node import *
from gestalt.Type import *
from gestalt.Generator import GestaltGenerator

from phoebusgen import screen

from gestalt.convert.phoebus.CSSWidget    import CSSWidget
from gestalt.convert.phoebus.CSSAnonGroup import CSSAnonGroup
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
			
				a_display.append(item.apply(the_generator, data=data))

						
	a_display.writeCSS(outputfile)
