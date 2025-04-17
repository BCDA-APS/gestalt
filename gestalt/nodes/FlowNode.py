from gestalt.Type import Number

from gestalt.nodes.GroupNode import GroupNode

class FlowNode(GroupNode):
	def __init__(self, name=None, layout={}, flow="vertical", loc=None):
		super(FlowNode, self).__init__("caFrame", name=name, layout=layout, loc=loc)
	
		self.makeInternal(Number, "padding",   0)
		self.makeInternal(Number, "last-pos",  0)
		self.setProperty("flow", flow, internal=True)

	def __iter__(self):
		return self.children.__iter__()
		
	def initApply(self, data):
		super().initApply(data)
		self["padding"].apply(data)
		self["last-pos"] = 0
		
	def positionNext(self, child):
		if self["flow"].val() == "vertical":
			child.position(x=None, y= self["last-pos"].val())
			self["last-pos"] = self["last-pos"].val() + child["geometry"]["height"] + int(self["padding"])
			
		elif self["flow"].val() == "horizontal":
			child.position(x=self["last-pos"].val(), y=None)
			self["last-pos"] = self["last-pos"].val() + child["geometry"]["width"] + int(self["padding"])
