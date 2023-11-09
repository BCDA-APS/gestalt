class DataType(object):
	def __init__(self, typ, val):
		self.typ = typ
		self.val = val
		self.defaultvalue = ""

	def apply(self, macros):
		if (type(self.val) is dict):
			for key, item in self.val.items():
				if item is None:
					self.val[key] = self.defaultvalue
				else:
					try:
						self.val[key] = str(item).format(**macros)
					except:
						pass
		else:
			try:
				self.val = str(self.val).format(**macros)
			except:
				pass
	
	def __setitem__(self, key, data):
		self.val[key] = data
		
	def __getitem__(self, key):
		return self.val[key]
		
	def merge(self, other):
		return type(self)(other.val)

		

###########################
#     BASIC DATA TYPES    #
###########################

class String(DataType):
	def __init__(self, val):
		super(String, self).__init__("string", val)		
	
class Number(DataType):
	def __init__(self, val):
		super(Number, self).__init__("number", val)
	
class Double(DataType):
	def __init__(self, val):
		super(Double, self).__init__("double", val)

class Enum(DataType):	
	def __init__(self, val):
		super(Enum, self).__init__("enum", val)

class Set(DataType):
	def __init__(self, val):
		super(Set, self).__init__("set", val)
	
class Bool(DataType):
	def __init__(self, val):
		super(Bool, self).__init__("bool", val)


###########################
#    GEOMETRY DATA TYPE   #
###########################


class Rect(DataType):			
	def __init__(self, *args, x=None, y=None, width=None, height=None):
		self.typ = "rect"
		self.defaultvalue = 0
		self.labels = ["x", "y", "width", "height"]
			
		if len(args) == 0:
			self.val = {"x" : x, "y" : y, "width" : width, "height" : height }
			return
			
		data = args
		
		if len(args) == 1:
			data = args[0]
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = [ int(item) for item in data.split("x")]
			
		temp = []
			
		for i in range(4 - len(data)):
			temp.append(None)
				
		for item in data:
			temp.append(item)
			
		self.val = dict(zip(self.labels, temp))

			
	def __getitem__(self, key):
		return int(self.val[key])
				
	def merge(self, other):	
		output = {}
		output.update(self.val)
					
		for key in self.labels:
			if other.val.get(key) is not None:
				output[key] = other.val[key]
			
		return Rect(output)

		
#######################
#   COLOR DATA TYPE   #
#######################

class Color(DataType):
	def __init__(self, *args, r=None, g=None, b=None, a=None):
		self.typ = "color"
		self.defaultvalue = 0
		self.labels = ["red", "green", "blue", "alpha"]
		
		if len(args) == 0:
			self.val = {"red" : r, "green" : g, "blue" : b, "alpha" : a}
			return
		
		data = args
		
		if len(args) == 1:
			data = args[0]
			
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = data.lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
			
		temp = [None, None, None, 255]
			
		for i in range(len(data)):
			temp[i] = data[i]
				
		self.val = dict( zip(self.labels, temp))
		
	def merge(self, other):
		output = {}
		output.update(self.val)
					
		for key in self.labels:
			if other.val.get(key) is not None:
				output[key] = other.val[key]
			
		return Color(output)
		
