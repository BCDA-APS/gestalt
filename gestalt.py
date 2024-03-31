#! /usr/bin/env python3

import os
import sys
import argparse
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
	
curr_dir = str(pathlib.Path(__file__).resolve().parent.resolve())

parser = argparse.ArgumentParser(prog='gestalt', usage='%(prog)s [OPTIONS] [TEMPLATE]', formatter_class=argparse.RawTextHelpFormatter, exit_on_error=False)

parser.add_argument("template", nargs="?", metavar="TEMPLATE", type=str, help="The template file used in constructing the output")
			
parser.add_argument("-f", "-r", "--from", "--read", 
	metavar="FORMAT", 
	dest="in_format",  
	action="store", 
	help="""
File parser that should be used for the input data file.

Recognized values are ['yml', 'yaml', 'string', 'str',
"json", "JSON", "substitutions", "msi", "auto"] 
(Default: 'auto')


""", 
	type=str,
	default="auto", 
	choices=["yml", "yaml", "string", "str", "JSON", "json", "substitutions", "msi", "auto"])
		
parser.add_argument("-t", "-w", "--to", "--write", 
	metavar="FORMAT",
	dest="out_format", 
	action="store", 
	help="""
File type conversion that should be used for the output 
UI file. 

Recognized values are ['qt', 'css', 'ui', 'bob', "auto"]
(Default: 'auto')


""", 
	type=str,
	default="auto", 
	choices=["qt", "bob", "ui", "css", "auto"])
			
parser.add_argument("-o", "--output",
	metavar="FILE",
	dest="out_filename",
	action="store",
	help="""
Output file name

(Default: Generate from template file and output format)


""",
	type=str)

parser.add_argument('-i', "--input",
	metavar="FILE",
	dest='in_filename',
	action='store', 
	help="""
Input data to apply to template file. Either a string
containing data in a yaml format, or the path to a
file to be parsed according to the input format.

(Default: Template will be applied with no macros)


""",
	type=str)

parser.add_argument("--include", 
	metavar="FOLDER", 
	dest="include_dirs", 
	action="append", 
help="""
Folders to search for any files included by the template.
Can be applied multiple times, one folder per argument.

By default, the search path includes the current directory 
and gestalt's template directory (for colors.yml).
	
	
""",
	type=str)



def doGenerate(args):
	include_dirs = [".", curr_dir + "/templates"]

	if args.include_dirs:
		include_dirs.extend(args.include_dirs)		

	data = {}	
	
	if args.in_filename:
		parse_format = args.in_format
	
		if args.in_format == "auto":
			parse_format = pathlib.PurePath(args.in_filename).suffix.lstrip('.')

		if parse_format == "string" or parse_format == "str":
			data = Datasheet.parseYAMLString(args.in_filename)
		elif parse_format == "yaml" or parse_format == "yml":
			data = Datasheet.parseYAMLFile(args.in_filename)
		elif parse_format == "json" or parse_format == "JSON":
			data = Datasheet.parseJSONFile(args.in_filename)
		elif parse_format == "msi" or parse_format == "substitutions":
			data = Datasheet.parseSubstitutionFile(args.in_filename)
		else:
			print("Unknown file extension: ", parse_format)
			return
	
	styles = Stylesheet.parse(args.template, include_dirs)
	
	if args.out_format == "auto":
		if not args.out_filename:
			print("Must specify either output file type or output file name")
			return
	
		args.out_format = pathlib.PurePath(args.out_filename).suffix.lstrip('.')
		
	if args.out_format == "qt":
		args.out_format = "ui"
	elif args.out_format == "css":
		args.out_format = "bob"
	
	if not args.out_filename:
		args.out_filename = pathlib.PurePath(args.template).stem + "." + args.out_format
	
	if args.out_format == "ui":
		generateQtFile(styles, data, outputfile=args.out_filename)
	elif args.out_format == "bob":
		generateCSSFile(styles, data, outputfile=args.out_filename)
	else:
		print("Unknown file extension: ", write_format)


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()
				
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
			constructed_args= [current_stylesheet, "-f",  "string"]
		
			if output_type == "CSS":
				constructed_args.extend(["-t", "css"])
			elif output_type == "Qt":
				constructed_args.extend(["-t", "qt"])
		
			constructed_args.extend(["-o", output_file])
			constructed_args.extend(["--input", self.InputData.toPlainText()])
		
			args = parser.parse_args(constructed_args)
			
			args.include_dirs = [".", curr_dir, curr_dir + "/templates", module_selected["path"]]
	
			doGenerate(args)

			self.Status.setText("File Generated")
			
		except Exception as e:
			traceback.print_exc()
			QMessageBox.warning(self, "Error Occured", str(e))


if __name__ == "__main__":
	args = parser.parse_args()	
	
	if (len(sys.argv) == 1):
		app = QApplication([])
		
		window = UI()
		app.exec_()
		
	elif args.template == None:
		print("Template file required for command-line conversion")
		
	else:
		doGenerate(args)
