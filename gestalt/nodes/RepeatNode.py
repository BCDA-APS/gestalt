from gestalt.nodes.LayoutNode import LayoutNode

class RepeatNode(LayoutNode):
	def __init__(self, name=None, layout={}, flow="vertical", loc=None):
		super(RepeatNode, self).__init__(name=name, layout=layout, loc=loc)
	
		self.setProperty("flow", flow, internal=True)
		
	def positionNext(self, line):
		if self["flow"].val() == "vertical":
			line.position(x=None, y= self["last-y"].val())
			self["last-y"] = self["last-y"].val() + line["geometry"]["height"] + int(self["padding"])
			
		elif self["flow"].val() == "horizontal":
			line.position(x=self["last-x"].val(), y=None)
			self["last-x"] = self["last-x"].val() + line["geometry"]["width"] + int(self["padding"])
