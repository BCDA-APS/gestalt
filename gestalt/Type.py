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
		elif isinstance(self.val, str):
			try:
				self.val = str(self.val).format(**macros)
			except KeyError:
				pass
	
	def __setitem__(self, key, data):
		self.val[key] = data
		
	def __getitem__(self, key):
		return self.val[key]

	def __bool__(self):
		return bool(self.val)
		
	def __int__(self):
		return int(self.val)
		
	def __str__(self):
		return str(self.val)
		
	def __float__(self):
		return float(self.val)
		
	def merge(self, other):
		return type(self)(other.val)

		

###########################
#     BASIC DATA TYPES    #
###########################

class String(DataType):
	def __init__(self, val):
		super(String, self).__init__("string", str(val))	
	
	def __bool__(self):
		output = super(String, self).__bool__()
		
		if output:
			try:
				output = bool(int(self.val.lower()))
			except:
				output = not ( self.val.lower() == "false" )
				
		return output
	
class Number(DataType):
	def __init__(self, val):
		super(Number, self).__init__("number", int(val))
	
class Double(DataType):
	def __init__(self, val):
		super(Double, self).__init__("double", float(val))

class Enum(DataType):	
	def __init__(self, val):
		super(Enum, self).__init__("enum", str(val))

class Set(DataType):
	def __init__(self, val):
		super(Set, self).__init__("set", str(val))
	
class Bool(DataType):
	def __init__(self, val):
		super(Bool, self).__init__("bool", bool(val))


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
			
		elif isinstance(data, Rect):
			data = data.val
			
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
		
		elif isinstance(data, String):
			data = data.val.lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
			
		elif isinstance(data, Color):
			self.val = data.val
			return
			
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
		

		
######################
#   FONT DATA TYPE   #
######################

class Font(DataType):
	def __init__(self, *args, family=None, style=None, size=None):
		self.typ = "font"
		self.defaultvalue = ""
		self.labels = ["family", "style", "size"]
		
		if len(args) == 0:
			self.val = {"family" : family, "style" : style.lower(), "size" : size}
			return
		
		data = args
		
		if len(args) == 1:
			data = args[0]
			
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):			
			data = [ item.strip() for item in data.lstrip("-").split("-") ]

		elif isinstance(data, Font):
			data = data.val
		
		temp = [None, None, None]
			
		for i in range(len(data)):
			temp[i] = data[i]
			
		self.val = dict(zip(self.labels, temp))
		
			
	def merge(self, other):
		output = {}
		output.update(self.val)
		
		for key in self.labels:
			if other.val.get(key) is not None:
				output[key] = other.val[key]
				
		return Font(output)
		
		
###########################
#   ALIGNMENT DATA TYPE   #
###########################

class Alignment(DataType):
	TOP = 0
	LEFT = 0
	CENTER = 1
	RIGHT = 2
	BOTTOM = 2
	
	
	def __init__(self, *args, horizontal="Center", vertical="Center"):
		self.typ = "align"
		self.defaultvalue = "Center"
		self.labels = [ "vertical", "horizontal" ]
		
		data = args
		
		if len(args) == 0:
			data = { "vertical" : vertical, "horizontal" : horizontal }
		
		if len(args) == 1:
			data = args[0]
			
		if isinstance(data, str):
			temp = { "vertical" : vertical, "horizontal" : horizontal }
				
			data = data.lower()
			
			if "top" in data:
				temp["vertical"] = "Top"
			if "bottom" in data:
				temp["vertical"] = "Bottom"
			if "left" in data:
				temp["horizontal"] = "Left"
			if "right" in data:
				temp["horizontal"] = "Right"
			
			data = temp
				
		if isinstance(data, dict):
			self.val = {}
			
			valign = str(data.get("vertical", "Center")).lower()
			halign = str(data.get("horizontal", "Center")).lower()
			
			if "top" in valign:
				self.val["vertical"] = Alignment.TOP
			elif "bottom" in valign:
				self.val["vertical"] = Alignment.BOTTOM
			else:
				self.val["vertical"] = Alignment.CENTER
				
			if "left" in halign:
				self.val["horizontal"] = Alignment.LEFT
			elif "right" in halign:
				self.val["horizontal"] = Alignment.RIGHT
			else:
				self.val["horizontal"] = Alignment.CENTER
			
		elif isinstance(data, Alignment):
			self.val = data.val
			
		

	def __str__(self):	
		valign = [ "Top", "Center", "Bottom" ]
		halign = [ "Left", "Center", "Right" ]
		
		return valign[self.val["vertical"]] + halign[self.val["horizontal"]]
			
