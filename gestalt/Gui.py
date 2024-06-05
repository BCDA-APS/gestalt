from PyQt5 import uic
from PyQt5 import QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel


class UI(QMainWindow):
	def __init__(self, curr_dir, genfunc, registry, parser):
		super(UI, self).__init__()
		self.genfunc = genfunc
		self.registry = registry
		self.parser = parser
		self.curr_dir = curr_dir
		
		uic.loadUi(curr_dir + "/.data/Form.ui", self)
		
		self.setWindowTitle("GESTALT")
			
		self.TemplateSelect.currentIndexChanged.connect(self.template_selected)
		#self.TemplateSelect.addItems(registry.templates.keys())
		
		self.TemplateType.currentIndexChanged.connect(self.type_selected)
		self.TemplateType.addItems(["Qt", "CSS"])
		
		self.LoadButton.clicked.connect(self.load_data)
		self.WriteButton.clicked.connect(self.write_data)
		
		self.show()

		
	def type_selected(self, selection):
		self.TemplateSelect.currentIndexChanged.disconnect(self.template_selected)
		self.TemplateSelect.clear()
		self.TemplateSelect.currentIndexChanged.connect(self.template_selected)
		
		output_type = self.TemplateType.itemText(selection)
		
		check_attr = ""
		
		if output_type == "Qt":
			check_attr = "qt_stylesheet"
		elif output_type == "CSS":
			check_attr = "css_stylesheet"
		
		for key, item in self.registry.templates.items():
			if check_attr in item:
				self.TemplateSelect.addItem(key)
		
	def template_selected(self, selection):
		module_selected = self.registry.templates[self.TemplateSelect.itemText(selection)]
		
		text = ""
		
		for item in module_selected["required_inputs"]:
			text += item[0]
			text += " - "
			text += item[1]
			text += "\n"

		self.TemplateInfo.setText(text)
		self.InputData.clear()
		self.InputData.appendPlainText(module_selected["example"])
		self.Status.setText("")
		self.TemplateThumbnail.setPixmap(QtGui.QPixmap(module_selected["thumbnail"]))
		
		
	def load_data(self):
		input_file = QFileDialog.getOpenFileName(self, "Open Input Data", filter="*.yml")[0]
		
		if input_file == "":
			return
			
		with open(input_file) as read_data:
			self.InputData.clear()
			self.InputData.appendPlainText(read_data.read())
			self.Status.setText(input_file + " loaded")
		
		
	def write_data(self):
		output_type = self.TemplateType.itemText(self.TemplateType.currentIndex())
		
		output_file = ""
		current_stylesheet = ""
		
		module_selected = self.registry.templates[self.TemplateSelect.itemText(self.TemplateSelect.currentIndex())]
		
		if output_type == "CSS":
			current_stylesheet = module_selected["css_stylesheet"]
			output_file = QFileDialog.getSaveFileName(self, "Save Generated File", "", filter="*.bob")[0]
		elif output_type == "Qt":
			current_stylesheet = module_selected["qt_stylesheet"]
			output_file = QFileDialog.getSaveFileName(self, "Save Generated File", "", filter="*.ui")[0]
		
		
		if output_file == "":
			return
		
		try:
			constructed_args= [current_stylesheet, "-f",  "string"]
		
			if output_type == "CSS":
				constructed_args.extend(["-t", "css"])
			elif output_type == "Qt":
				constructed_args.extend(["-t", "qt"])
		
			constructed_args.extend(["-o", output_file])
			constructed_args.extend(["--input", self.InputData.toPlainText()])
		
			args = self.parser.parse_args(constructed_args)
			
			args.include_dirs = [".", self.curr_dir, self.curr_dir + "/templates", module_selected["path"]]
	
			self.genfunc(args)

			self.Status.setText("File Generated")
			
		except Exception as e:
			traceback.print_exc()
			QMessageBox.warning(self, "Error Occured", str(e))
