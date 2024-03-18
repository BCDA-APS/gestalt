class DataType(object):
	def __init__(self, typ, val):
		self.typ = typ
		self.value = val
		self.defaultvalue = ""
		self.applied = False

	def apply(self, macros):		
		self.applied = True
		
		if (type(self.value) is dict):
			for key, item in self.value.items():
				if item is None:
					self.value[key] = self.defaultvalue
				else:
					try:
						self.value[key] = str(item).format(**macros)
					except:
						pass
		elif isinstance(self.value, str):
			try:
				self.value = str(self.value).format(**macros)
			except KeyError:
				pass
				
	def val(self):
		if not self.applied:
			self.apply({})
		
		return self.value
	
	def __setitem__(self, key, data):
		self.val()[key] = data
		
	def __getitem__(self, key):
		return self.val()[key]

	def __bool__(self):
		return bool(self.value)
		
	def __int__(self):
		return int(self.value)
		
	def __str__(self):
		return str(self.value)
		
	def __float__(self):
		return float(self.value)
		

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
		#self.typ = "rect"
		#self.defaultvalue = 0
		#self.labels = ["x", "y", "width", "height"]
			
		# if len(args) == 0:
			# self.value = {"x" : x, "y" : y, "width" : width, "height" : height }
			# return
			
		# data = args
		
		# if len(args) == 1:
			# data = args[0]
		
		# if isinstance(data, dict):
			# data = [ data.get(key, self.defaultvalue) for key in self.labels ]
		
		# elif isinstance(data, str):
			# data = [ int(item) for item in data.split("x")]
			
		# elif isinstance(data, Rect):
			# self.value = data.val
			# return
			
		# temp = []
			
		# for i in range(4 - len(data)):
			# temp.append(self.defaultvalue)
				
		# for item in data:
			# temp.append(item)
			
		# self.value = dict(zip(self.labels, temp))
		
	def apply(self, macros):
		super(Rect, self).apply(macros)
		
		self.labels = ["x", "y", "width", "height"]
			
		data = self.value
		
		if isinstance(data, dict):
			data = [ data.get(key, 0) for key in self.labels ]
		
		elif isinstance(data, str):
			data = [ int(item) for item in data.split("x")]
		
		elif isinstance(data, String):
			data.apply(macros)
			data = [ int(item) for item in data.val().split("x") ]
			
		elif isinstance(data, Rect):
			data.apply(macros)
			self.value = data.val()
			return
			
		temp = []
			
		for i in range(4 - len(data)):
			temp.append(0)
				
		for item in data:
			temp.append(item)
			
		self.value = dict(zip(self.labels, temp))
		
	def __getitem__(self, key):
		return int(self.val()[key])
						
#######################
#   COLOR DATA TYPE   #
#######################

class Color(DataType):
	def __init__(self, *args, r=None, g=None, b=None, a=None):
		super(Color, self).__init__("color", *args)
		# self.typ = "color"
		# self.defaultvalue = 0
		# self.labels = ["red", "green", "blue", "alpha"]
		
		# if len(args) == 0:
			# self.value = {"red" : r, "green" : g, "blue" : b, "alpha" : a}
			# return
		
		# data = args
		
		# if len(args) == 1:
			# data = args[0]
			
		# if isinstance(data, dict):
			# data = [ data.get(key, None) for key in self.labels ]
		
		# elif isinstance(data, str):
			# data = data.lstrip("$")
			
			# # Interpret each 2-char chunk as a hex number
			# data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
		
		# elif isinstance(data, String):
			# data = data.val.lstrip("$")
			
			# # Interpret each 2-char chunk as a hex number
			# data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
			
		# elif isinstance(data, Color):
			# self.value = data.val
			# return
			
		# temp = [None, None, None, 255]
			
		# for i in range(len(data)):
			# temp[i] = data[i]
				
		# self.value = dict( zip(self.labels, temp))
		
	def apply(self, macros):
		super(Color, self).apply(macros)
		
		self.labels = ["red", "green", "blue", "alpha"]
		
		data = self.value
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = data.lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
		
		elif isinstance(data, String):
			data.apply(macros)
			data = data.val().lstrip("$")
			
			# Interpret each 2-char chunk as a hex number
			data = [ int(data[i:i+2], 16) for i in range(0, len(data), 2) ]
			
		elif isinstance(data, Color):
			data.apply(macros)
			self.value = data.val()
			return
			
		temp = [None, None, None, 255]
			
		for i in range(len(data)):
			temp[i] = data[i]
				
		self.value = dict( zip(self.labels, temp))
		
		
######################
#   FONT DATA TYPE   #
######################

class Font(DataType):
	def __init__(self, *args, family=None, style=None, size=None):
		super(Font, self).__init__("font", *args)
		# self.typ = "font"
		# self.defaultvalue = ""
		# self.labels = ["family", "style", "size"]
		
		# if len(args) == 0:
			# self.value = {"family" : family, "style" : style.lower(), "size" : size}
			# return
		
		# data = args
		
		# if len(args) == 1:
			# data = args[0]
			
		# if isinstance(data, dict):
			# data = [ data.get(key, None) for key in self.labels ]
		
		# elif isinstance(data, str):
			# data = [ item.strip() for item in data.lstrip("-").split("-") ]
			
		# elif isinstance(data, String):
			# data = [ item.strip() for item in data.val.lstrip("-").split("-") ]

		# elif isinstance(data, Font):
			# self.value = data.val
			# return
		
		# temp = [None, None, None]
			
		# for i in range(len(data)):
			# temp[i] = data[i]
			
		# self.value = dict(zip(self.labels, temp))
		
	def apply(self, macros):
		super(Font, self).apply(macros)
		
		self.labels = ["family", "style", "size"]
		
		data = self.value
		
		if isinstance(data, dict):
			data = [ data.get(key, None) for key in self.labels ]
		
		elif isinstance(data, str):
			data = [ item.strip() for item in data.lstrip("-").split("-") ]
			
		elif isinstance(data, String):
			data = [ item.strip() for item in data.val.lstrip("-").split("-") ]

		elif isinstance(data, Font):
			data.apply(macros)
			self.value = data.val()
			return
		
		temp = [None, None, None]
			
		for i in range(len(data)):
			temp[i] = data[i]
			
		self.value = dict(zip(self.labels, temp))
		
		
		
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
		super(Alignment, self).__init__("align", *args)
		# self.typ = "align"
		# self.defaultvalue = "Center"
		# self.labels = [ "vertical", "horizontal" ]
		
		# data = args
		
		# if len(args) == 0:
			# data = { "vertical" : vertical, "horizontal" : horizontal }
		
		# if len(args) == 1:
			# data = args[0]
			
		# if isinstance(data, str):
			# temp = { "vertical" : vertical, "horizontal" : horizontal }
				
			# data = data.lower()
			
			# if "top" in data:
				# temp["vertical"] = "Top"
			# if "bottom" in data:
				# temp["vertical"] = "Bottom"
			# if "left" in data:
				# temp["horizontal"] = "Left"
			# if "right" in data:
				# temp["horizontal"] = "Right"
			
			# data = temp
				
		# if isinstance(data, dict):
			# self.value = {}
			
			# valign = str(data.get("vertical", "Center")).lower()
			# halign = str(data.get("horizontal", "Center")).lower()
			
			# if "top" in valign:
				# self.value["vertical"] = Alignment.TOP
			# elif "bottom" in valign:
				# self.value["vertical"] = Alignment.BOTTOM
			# else:
				# self.value["vertical"] = Alignment.CENTER
				
			# if "left" in halign:
				# self.value["horizontal"] = Alignment.LEFT
			# elif "right" in halign:
				# self.value["horizontal"] = Alignment.RIGHT
			# else:
				# self.value["horizontal"] = Alignment.CENTER
			
		# elif isinstance(data, Alignment):
			# self.value = data.val
			
	
	def apply(self, macros):
		super(Alignment, self).apply(macros)
		
		self.labels = [ "vertical", "horizontal" ]
		
		data = self.value
		
		if isinstance(data, str):
			temp = { "vertical" : None, "horizontal" : None }
				
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
			self.value = {}
			
			valign = str(data.get("vertical", "Center")).lower()
			halign = str(data.get("horizontal", "Center")).lower()
			
			if "top" in valign:
				self.value["vertical"] = Alignment.TOP
			elif "bottom" in valign:
				self.value["vertical"] = Alignment.BOTTOM
			else:
				self.value["vertical"] = Alignment.CENTER
				
			if "left" in halign:
				self.value["horizontal"] = Alignment.LEFT
			elif "right" in halign:
				self.value["horizontal"] = Alignment.RIGHT
			else:
				self.value["horizontal"] = Alignment.CENTER
			
		elif isinstance(data, Alignment):
			data.apply(macros)
			self.value = data.val()
		

	def __str__(self):	
		valign = [ "Top", "Center", "Bottom" ]
		halign = [ "Left", "Center", "Right" ]
		
		return valign[self.value["vertical"]] + halign[self.value["horizontal"]]
			
