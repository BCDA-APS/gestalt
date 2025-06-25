import tkinter as tk
import tkinter.font as tkfont

DEFAULT_DPI = 96.0

size_cache = {}

class GestaltGenerator:
	def get_font_height(font_name, font_size):
		if font_name not in size_cache:
			size_cache[font_name] = {}
			
		if font_size in size_cache[font_name]:
			return size_cache[font_name][font_size]
		
		tk_root = tk.Tk()
		tk_root.withdraw()
		
		tk_font = tkfont.Font(family=font_name, size=font_size)
		
		dpi_scale = DEFAULT_DPI / tk_root.winfo_fpixels("1i")
		
		ascent = round(tk_font.metrics("ascent") * dpi_scale)
		descent = round(tk_font.metrics("descent") * dpi_scale)
		
		tk_root.destroy()
		
		size_cache[font_name][font_size] = int(ascent + descent)
		
		return int(ascent + descent)
		
	def get_size_for_height(font_name, height):
		needed_height = int(height * 0.75)
		
		lower_bound = 6
		upper_bound = -1
		
		while True:
			upper_bound = lower_bound * 2
			
			estimated_size = GestaltGenerator.get_font_height(font_name, upper_bound)
			
			if estimated_size == needed_height:
				return upper_bound
			
			if estimated_size > needed_height:
				break
				
			lower_bound = upper_bound
		
		while True:
			check = int((lower_bound + upper_bound) / 2)
			
			if check == lower_bound:
				return lower_bound
				
			estimated_size = GestaltGenerator.get_font_height(font_name, check)
				
			if estimated_size == needed_height:
				return check
			elif estimated_size < needed_height:
				lower_bound = check
			else:
				upper_bound = check
		
	def get_text_width(font_name, font_size, text):
		tk_root = tk.Tk()
		tk_root.withdraw()
		
		tk_font = tkfont.Font(family=font_name, size=font_size)
		
		dpi_scale = DEFAULT_DPI / tk_root.winfo_fpixels("1i")
		
		output = tk_font.measure(text) * dpi_scale
		
		tk_root.destroy()
		
		return output
	
	
	def generateWidget(self, original, macros={}):
		pass
		
	def generateGroup(self, original, macros={}):
		pass
	
	def generateAnonymousGroup(self, macros={}):
		pass		
	
	def generateRelatedDisplay(self, node, macros={}):
		pass

	def generateMessageButton(self, node, macros={}):
		pass

	def generateText(self, node, macros={}):
		pass
		
	def generateTextEntry(self, node, macros={}):
		pass
		
	def generateTextMonitor(self, node, macros={}):
		pass

	def generateMenu(self, node, macros={}):
		pass

	def generateChoiceButton(self, node, macros={}):
		pass

	def generateLED(self, node, macros={}):
		pass

	def generateByteMonitor(self, node, macros={}):
		pass

	def generateRectangle(self, node, macros={}):
		pass

	def generateEllipse(self, node, macros={}):
		pass

	def generateArc(self, node, macros={}):
		pass
		
	def generatePolygon(self, node, macros={}):
		pass
		
	def generatePolyline(self, node, macros={}):
		pass

	def generateImage(self, node, macros={}):
		pass

	def generateSlider(self, node, macros={}):
		pass

	def generateScale(self, node, macros={}):
		pass

	def generateShellCommand(self, node, macros={}):
		pass

	def generateTabbedGroup(self, node, macros={}):
		pass

	def generateCalc(self, node, macros={}):
		pass

	def generateInclude(self, node, macros={}):
		pass
