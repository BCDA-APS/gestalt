#! /APSshare/anaconda3/x86_64/bin/python3

import os
import tempfile
import traceback

from templates import *
from gestalt import *


from PyQt5 import uic
from PyQt5 import QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
	

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()
		uic.loadUi(".data/Form.ui", self)
		
		self.setWindowTitle("GESTALT")
		
		self.TemplateSelect.currentIndexChanged.connect(self.template_selected)
		self.TemplateSelect.addItems(registry.templates.keys())
		
		self.LoadButton.clicked.connect(self.load_data)
		self.WriteButton.clicked.connect(self.write_data)
		
		self.show()

		
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
		output_file = QFileDialog.getSaveFileName(self, "Save Generated File", "", filter="*.ui")[0]
		
		if output_file == "":
			return
		
		module_selected = registry.templates[self.TemplateSelect.itemText(self.TemplateSelect.currentIndex())]
		
		current_stylesheet = module_selected["stylesheet"]
		
		try:
			Gestalt.generateQtFile(stylesheet=current_stylesheet, datastr=self.InputData.toPlainText(), outputfile=output_file, searchpath="./templates")
			self.Status.setText("File Generated")
			
		except Exception as e:
			traceback.print_exc()
			QMessageBox.warning(self, "Error Occured", str(e))
		
		

app = QApplication([])

window = UI()
app.exec_()
