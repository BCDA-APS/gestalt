class DataType(object):
	def __init__(self, typ, val):
		self.typ = typ
		self.val = val
		self.defaultvalue = ""
		
				
	def write(self, tree):
		tree.start(self.typ, {})
		
		if (type(self.val) is dict):
			for key, item in self.val.items():
				tree.start(key, {})
				
				if item is None:
					tree.data(str(self.defaultvalue))
				else:	
					tree.data(str(item))
					
				tree.end(key)
		else:
			tree.data(str(self.val))
			
		tree.end(self.typ)
		
	def merge(self, other):
		return type(self)(other.val)

		

"""
	BASIC DATA TYPES
"""
class String(DataType):
	def __init__(self, val):
		super(String, self).__init__("string", val)		
	
class Number(DataType):
	def __init__(self, val):
		super(Number, self).__init__("number", val)

class Enum(DataType):	
	def __init__(self, val):
		super(Enum, self).__init__("enum", val)

class Set(DataType):
	def __init__(self, val):
		super(Set, self).__init__("set", val)
	
	
"""
	GEOMETRY DATA TYPE
"""
class Rect(DataType):			
	def __init__(self, *args, x=None, y=None, width=None, height=None):
		self.typ = "rect"
		self.defaultvalue = 0
			
		if len(args) == 0:
			self.val = {"x" : x, "y" : y, "width" : width, "height" : height }
			return
			
		data = args[0]
		
		if isinstance(data, dict):
			self.val = {
				"x" : data.get("x", None), 
				"y" : data.get("y", None),
				"width" : data.get("width", data.get("wid", None)), 
				"height" : data.get("height", data.get("hei", None))}
			
		elif isinstance(data, list) or isinstance(data, tuple):
			temp = []
			
			for i in range(4 - len(data)):
				temp.append(None)
				
			for item in data:
				temp.append(item)
			
			self.val = {
				"x" : temp[0],
				"y" : temp[1],
				"width" : temp[2],
				"height" : temp[3] }
					
		elif isinstance(data, str):
			wid, hei = map(int, data.split("x"))
			
			self.val = { "width" : wid, "height" : hei }
					
		elif isinstance(data, int):
			temp = []
			for i in range(4 - len(args)):
				temp.append(None)
				
			for item in args:
				temp.append(item)
				
			self.val = {
				"x" : temp[0],
				"y" : temp[1],
				"width" : temp[2],
				"height" : temp[3] }
	
				
	def merge(self, other):	
		output = {}
		output.update(self.val)
					
		if not other.val.get("x") is None:
			output["x"] = other.val["x"]
		
		if not other.val.get("y") is None:
			output["y"] = other.val["y"]
				
		if not other.val.get("width") is None:
			output["width"] = other.val["width"]
		
		if not other.val.get("height") is None:
			output["height"] = other.val["height"]
			
		return Rect(output)

		
"""
	COLOR DATA TYPE
"""
class Color(DataType):
	def __init__(self, *args, r=None, g=None, b=None, a=None):
		self.typ = "color"
		self.defaultvalue = 0
		
		if len(args) == 0:
			
			if a is None:
				self.alpha = 255
			else:
				self.alpha = a
				
			self.val = {"red" : r, "green" : g, "blue" : b}
			return
		
		data = args[0]
		
		if isinstance(data, dict):
			self.alpha = params.get("a", params.get("alpha", None))
		
			self.val = {
				"red"   : params.get("r", params.get("red", None)),
				"green" : params.get("g", params.get("green", None)),
				"blue"  : params.get("b", params.get("blue", None)) }
			
		elif isinstance(data, list) or isinstance(data, tuple):
			temp = [None, None, None, 255]
			
			for i in range(len(params)):
				temp[i] = params[i]
				
			self.alpha = temp[3]
			self.val = { 
				"red"   : temp[0],
				"green" : temp[1], 
				"blue"  : temp[2] }
					
		elif isinstance(data, str):
			data = data.lstrip("$")
			
			temp = [0, 0, 0, 255]
			
			for i in range(0, len(data), 2):
				temp[int(i/2)] = int(data[i:i+2], 16)
			
			self.alpha = temp[3]
			self.val = { 
				"red"   : temp[0],
				"green" : temp[1], 
				"blue"  : temp[2] }
					
		elif isinstance(data, int):
			temp = [0, 0, 0, 255]
					
			int i = 0
			for item in args:
				temp[i] = item
				i += 1
				
				if i >= 4:
					break

			self.alpha = temp[3]
			self.val = {
				"red"   : temp[0],
				"green" : temp[1],
				"blue"  : temp[2] }
				
					
	def write(self, tree):
		tree.start(self.typ, {"alpha" : str(self.alpha)})
		
		for key, item in self.val.items():
			tree.start(key, {})
			tree.data(str(item))
			tree.end(key)
			
		tree.end(self.typ)

		
	def merge(self, other):
		r_out = self.val["red"]
		g_out = self.val["green"]
		b_out = self.val["blue"]
		a_out = self.alpha
		
		if not other.val.get("red") is None:
			r_out = other.val["red"]
		
		if not other.val.get("green") is None:
			g_out = other.val["green"]
				
		if not other.val.get("blue") is None:
			b_out = other.val["blue"]
		
		if not other.alpha is None:
			a_out = other.alpha
			
		return Color(r=r_out, g=g_out, b=b_out, a=a_out)
		
