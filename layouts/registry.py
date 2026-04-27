from pathlib import Path

class Input:
	def __init__(self, name, info):
		self.name = name
		self.description = info

templates = {}

def add(name, path='', qt_stylesheet=None, css_stylesheet=None, pydm_stylesheet=None, required_inputs=[], example=''):
	data = {}
	base = Path(path[0])
	data["path"] = path[0]
	
	if qt_stylesheet:
		data["qt_stylesheet"] = str(base / str(qt_stylesheet))
	
	if css_stylesheet:
		data["css_stylesheet"] = str(base / str(css_stylesheet))
		
	if pydm_stylesheet:
		data["pydm_stylesheet"] = str(base / str(pydm_stylesheet))
		
	data["thumbnail"] = str(base / "thumbnail.png")
	data["required_inputs"] = required_inputs
	data["example"] = example

	templates[name] = data
