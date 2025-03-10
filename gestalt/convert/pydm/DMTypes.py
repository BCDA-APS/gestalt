from gestalt.Type import *

class Brush(Color):
	def __init__(self, data):
		super().__init__(data)

class Size(Rect):
	def __init__(self, data):
		super().__init__(data)
		self.typ = "size"
	
	def val(self):
		output = super().val()
		return { "width" : output["width"], "height" : output["height"] }
