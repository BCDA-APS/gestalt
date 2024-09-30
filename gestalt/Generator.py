import tkinter as tk
import tkinter.font as tkfont

DEFAULT_DPI = 96.0

class GestaltGenerator:
	def get_font_height(font_name, font_size):
		tk_root = tk.Tk()
		tk_root.withdraw()
		
		tk_font = tkfont.Font(family=font_name, size=font_size)
		
		dpi_scale = DEFAULT_DPI / tk_root.winfo_fpixels("1i")
		
		ascent = round(tk_font.metrics("ascent") * dpi_scale)
		descent = round(tk_font.metrics("descent") * dpi_scale)
		
		tk_root.destroy()
		
		return int(ascent + descent)
		
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
