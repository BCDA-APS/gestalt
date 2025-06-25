#! /usr/bin/env python3

import os
import sys
import argparse
import pathlib
import tempfile
import traceback
#import cProfile

from layouts import *
from gestalt import Datasheet, Stylesheet


curr_dir = str(pathlib.Path(__file__).resolve().parent.resolve())

parser = argparse.ArgumentParser(prog='gestalt', usage='%(prog)s [OPTIONS] [LAYOUT]', formatter_class=argparse.RawTextHelpFormatter, exit_on_error=False)

parser.add_argument("layout", nargs="?", metavar="LAYOUT", type=str, help="The layout file used in constructing the output")
			
parser.add_argument("-f", "-r", "--from", "--read", 
	metavar="FORMAT", 
	dest="in_format",  
	action="store", 
	help="""
File parser that should be used for the input data file.

Recognized values are ['yml', 'yaml', 'string', 'str',
"json", "JSON", "substitutions", "msi", "ini", "cfg", "auto"] 
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

Recognized values are ['qt', 'css', 'ui', 'bob', "pydm", "dm", "auto"]
(Default: 'auto')


""", 
	type=str,
	default="auto", 
	choices=["qt", "bob", "ui", "css", "pydm", "dm", "auto"])
			
parser.add_argument("-o", "--output",
	metavar="FILE",
	dest="out_filename",
	action="store",
	help="""
Output file name

(Default: Generate from layout file and output format)


""",
	type=str)

parser.add_argument('-i', "--input",
	metavar="FILE",
	dest='in_filename',
	action='store', 
	help="""
Input data to apply to layout file. Either a string
containing data in a yaml format, or the path to a
file to be parsed according to the input format.

(Default: Layout will be applied with no macros)


""",
	type=str)

parser.add_argument("--include", 
	metavar="FOLDER", 
	dest="include_dirs", 
	action="append", 
help="""
Folders to search for any files included by the layout.
Can be applied multiple times, one folder per argument.

By default, the search path includes the current directory 
and gestalt's widgets directory (for colors.yml).
	
	
""",
	type=str)



def doGenerate(args):
	include_dirs = [".", curr_dir + "/widgets"]

	if args.include_dirs:
		include_dirs.extend(args.include_dirs)		

	data = {}	
	
	if args.in_filename:
		parse_format = args.in_format
	
		if args.in_format == "auto":
			parse_format = pathlib.PurePath(args.in_filename).suffix.lstrip('.')

		if parse_format == "string" or parse_format == "str" or parse_format=="":
			data = Datasheet.parseYAMLString(args.in_filename)
		elif parse_format == "yaml" or parse_format == "yml":
			data = Datasheet.parseYAMLFile(args.in_filename)
		elif parse_format == "json" or parse_format == "JSON":
			data = Datasheet.parseJSONFile(args.in_filename)
		elif parse_format == "msi" or parse_format == "substitutions":
			data = Datasheet.parseSubstitutionFile(args.in_filename)
		elif parse_format == "ini" or parse_format == "cfg":
			data = Datasheet.parseINIFile(args.in_filename)
		else:
			print("Unknown file extension: ", parse_format)
			return
	
	styles = Stylesheet.parse(args.layout, include_dirs)
	
	if args.out_format == "auto":
		if not args.out_filename:
			print("Must specify either output file type or output file name")
			return
	
		args.out_format = pathlib.PurePath(args.out_filename).suffix.lstrip('.')
		
	if args.out_format == "qt":
		args.out_format = "ui"
	elif args.out_format == "css":
		args.out_format = "bob"
	elif args.out_format == "pydm":
		args.out_format = "dm"
		
	
	if not args.out_filename:
		args.out_filename = pathlib.PurePath(args.layout).stem + "." + args.out_format
	
	if args.out_format == "ui":
		from gestalt.convert.qt.QtGenerator import generateQtFile

		generateQtFile(styles, data, outputfile=args.out_filename)
	elif args.out_format == "bob":
		from gestalt.convert.phoebus.CSSGenerator import generateCSSFile
			
		generateCSSFile(styles, data, outputfile=args.out_filename)
	elif args.out_format == "dm":
		from gestalt.convert.pydm.DMGenerator import generateDMFile
		
		generateDMFile(styles, data, outputfile=args.out_filename)
		
	else:
		print("Unknown file extension: ", write_format)


if __name__ == "__main__":
	args = parser.parse_args()	
	
	if (len(sys.argv) == 1):
		from gestalt.Gui import UI
		from PyQt5.QtWidgets import *
	
		app = QApplication([])
		
		window = UI(curr_dir, doGenerate, registry, parser)
		app.exec_()
		
	elif args.layout == None:
		print("Layout file required for command-line conversion")
		
	else:
		#cProfile.run("doGenerate(args)")
		doGenerate(args)
