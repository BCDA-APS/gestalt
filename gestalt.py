#! /usr/bin/env python3

import os
import pathlib
import tempfile
import traceback

from templates import *
from gestalt import *

from gestalt.convert.qt.QtGenerator import generateQtFile
from gestalt.convert.phoebus.CSSGenerator import generateCSSFile

from PyQt5 import uic
from PyQt5 import QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
	

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()
		
		self.curr_dir = str(pathlib.Path(__file__).resolve().parent.resolve())
		
		uic.loadUi(self.curr_dir + "/.data/Form.ui", self)
		
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
		
		for key, item in registry.templates.items():
			if check_attr in item:
				self.TemplateSelect.addItem(key)
		
	def template_selected(self, selection):
		module_selected = registry.templates[self.TemplateSelect.itemText(selection)]
		
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
		
		module_selected = registry.templates[self.TemplateSelect.itemText(self.TemplateSelect.currentIndex())]
		
		if output_type == "CSS":
			current_stylesheet = module_selected["css_stylesheet"]
			output_file = QFileDialog.getSaveFileName(self, "Save Generated File", "", filter="*.bob")[0]
		elif output_type == "Qt":
			current_stylesheet = module_selected["qt_stylesheet"]
			output_file = QFileDialog.getSaveFileName(self, "Save Generated File", "", filter="*.ui")[0]
		
		
		if output_file == "":
			return
		
		try:			
			includes_dirs = str.split(".:" + self.curr_dir + ":" + self.curr_dir + "/templates:" + module_selected["path"], ":")
							
			styles = Stylesheet.parse(current_stylesheet, includes_dirs)
			data = Datasheet.parseString(self.InputData.toPlainText())
		
				
			if output_type == "CSS":
				generateCSSFile(styles, data, outputfile=output_file)
			if output_type == "Qt":
				generateQtFile(styles, data, outputfile=output_file)

			self.Status.setText("File Generated")
			
		except Exception as e:
			traceback.print_exc()
			QMessageBox.warning(self, "Error Occured", str(e))
		
		

app = QApplication([])

window = UI()
app.exec_()
