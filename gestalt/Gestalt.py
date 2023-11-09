from gestalt import Stylesheet
from gestalt import Datasheet

from gestalt.convert.qt.QtGenerator import generateQtFile
		
def generateFile(stylesheet="", datafile="", datastr="", outputfile="", searchpath=""):	
	includes_dirs = str.split(".:" + searchpath, ":")
	
	styles = Stylesheet.parse(stylesheet, includes_dirs)
	data = None
	
	if datafile != "":
		data = Datasheet.parseFile(datafile)
	else:
		data = Datasheet.parseString(datastr)
		
	generateQtFile(styles, data, outputfile=outputfile)
