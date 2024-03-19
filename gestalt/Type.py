import copy

class DataType(object):
	def __init__(self, typ, val):
		self.typ = typ
		self.value = val
		self.defaultvalue = ""
		self.macros = {}
		self.updates = {}

	def apply(self, macros):		
		self.macros = copy.deepcopy(macros)
				
	def val(self):
		output = copy.deepcopy(self.value)
		
		if (type(output) is dict):
			for key, item in output.items():
				if item is None:
					output[key] = self.defaultvalue
				else:
					try:
						output[key] = str(item).format(**self.macros)
					except:
						pass
		elif isinstance(output, str):
			try:
				output = str(self.value).format(**self.macros)
			except KeyError:
				pass
	
		return output
	
	def __setitem__(self, key, data):
		self.updates[key] = data
		
	def __getitem__(self, key):
		return self.val()[key]

	def __bool__(self):
		return bool(self.val())
		
	def __int__(self):
		return int(self.val())
		
	def __str__(self):
		return str(self.val())
		
	def __float__(self):
		return float(self.val())
		

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
				output = bool(int(self.value.lower()))
			except:
				output = not ( self.value.lower() == "false" )
				
		return output
	
class Number(DataType):
	def __init__(self, val):
		super(Number, self).__init__("number", val)
		
	def val(self):
		return int(self.value)
	
class Double(DataType):
	def __init__(self, val):
		super(Double, self).__init__("double", val)
		
	def val(self):
		return float(self.value)

class Enum(DataType):	
	def __init__(self, val):
		super(Enum, self).__init__("enum", val)
		
	def val(self):
		return str(self.value)

class Set(DataType):
	def __init__(self, val):
		super(Set, self).__init__("set", val)
		
	def val(self):
		return str(self.value)
	
class Bool(DataType):
	def __init__(self, val):
		super(Bool, self).__init__("bool", val)
		
	def val(self):
		return bool(self.value)

class Not(DataType):
	def __init__(self, val):
		super(Not, self).__init__("inverse", val)
		
	def val(self):
		return str(self.value)
	

###########################
#    GEOMETRY DATA TYPE   #
###########################


class Rect(DataType):			
	def __init__(self, *args, x=0, y=0, width=0, height=0):
		super(Rect, self).__init__("rect", *args)
		
	def val(self):
		self.labels = ["x", "y", "width", "height"]
			
		data = super(Rect, self).val()
		
		if isinstance(data, dict):
			data = [ data.get(key, 0) for key in self.labels ]
				
		elif isinstance(data, int):
			# int indicates the parser read a value like 0x123 as a hex value
			data = [ 0, '{:x}'.format(data) ]
			
		elif isinstance(data, Number):
			data.apply(self.macros)
			data = [ 0, '{:x}'.format(int(data)) ]
		
		elif isinstance(data, str):
			data = [ int(item) for item in data.split("x")]
		
		elif isinstance(data, String):
			data.apply(self.macros)
			data = [ int(item) for item in data.val().split("x") ]
			
		elif isinstance(data, Rect):
			data.apply(self.macros)
			output = data.val()
			output.update(self.updates)
			return output
			
		temp = []
			
		for i in range(4 - len(data)):
			temp.append(0)
				
		for item in data:
			temp.append(item)
			
		output = dict(zip(self.labels, temp))
		output.update(self.updates)
		return output
		
	def __getitem__(self, key):
		return int(self.val()[key])
						
#######################
#   COLOR DATA TYPE   #
#######################

class Color(DataType):
	def __init__(self, *args, r=None, g=None, b=None, a=None):
		super(Color, self).__init__("color", *args)
		
	def val(self):
		self.labels = ["red", "green", "blue", "alpha"]
		
		data = super(Color, self).val()
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = data.lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
		
		elif isinstance(data, String):
			data.apply(self.macros)
			data = data.val().lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
			
		elif isinstance(data, Color):
			data.apply(self.macros)
			output = data.val()
			output.update(self.updates)
			return output
			
		temp = [None, None, None, 255]
			
		for i in range(len(data)):
			temp[i] = data[i]
				
		output = dict( zip(self.labels, temp))
		output.update(self.updates)
		return output
		
		
######################
#   FONT DATA TYPE   #
######################

class Font(DataType):
	def __init__(self, *args, family=None, style=None, size=None):
		super(Font, self).__init__("font", *args)
		
	def val(self):
		self.labels = ["family", "style", "size"]
		
		data = super(Font, self).val()
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = [ item.strip() for item in data.lstrip("-").split("-") ]
			
		elif isinstance(data, String):
			data = [ item.strip() for item in data.val.lstrip("-").split("-") ]

		elif isinstance(data, Font):
			data.apply(self.macros)
			return data.val()
		
		temp = [None, None, None]
			
		for i in range(len(data)):
			temp[i] = data[i]
			
		return dict(zip(self.labels, temp))
		
		
		
###########################
#   ALIGNMENT DATA TYPE   #
###########################

class Alignment(DataType):	
	def __init__(self, *args, horizontal="Center", vertical="Center"):
		super(Alignment, self).__init__("align", *args)		
	
	def val(self):
		self.labels = [ "vertical", "horizontal" ]
		
		data = super(Alignment, self).val()
		
		if isinstance(data, str):
			temp = { "vertical" : "Center", "horizontal" : "Center" }
				
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
			temp = { "vertical" : "Center", "horizontal" : "Center"}
			
			if "vertical" in data:
				temp["vertical"] = str(data["vertical"]).capitalize()
			
			if "horizontal" in data:
				temp["horizontal"] = str(data["horizontal"]).capitalize()
					
			temp.update(self.updates)
			return temp
			
		elif isinstance(data, Alignment):
			data.apply(self.macros)
			output = data.val()
			output.update(self.updates)
			return output
		

	def __str__(self):	
		return str(self.val()["vertical"]) + str(self.val()["horizontal"])
			
