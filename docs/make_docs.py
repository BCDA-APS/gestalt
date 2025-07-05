#! /usr/bin/env python3

import os
import ast
import glob
	
def generate(package):
	index = 1
	
	for file in sorted(glob.glob("../gestalt/" + package + "/*.py")):
		modulename = os.path.splitext(os.path.basename(file))[0]
		
		if modulename == "__init__":
			continue
		
		print("Generating: " + modulename)
			
		info = "title='{}' parent='{}' nav_order={}".format(modulename, package.capitalize(), index)
		
		output_path = "./reference/" + package + "/" + modulename + ".md"
		
		with open(file, "r") as the_module:
			contents = the_module.read()
			
			module = ast.parse(contents)
			
		
			with open(output_path, "w") as the_file:
				the_file.write("---\n")
				the_file.write("layout: default\n")
				the_file.write("title: " + modulename + "\n")
				the_file.write("parent: " + package.capitalize() + "\n")
				the_file.write("nav_order: " + str(index) + "\n")
				the_file.write("has_toc: false\n")
				the_file.write("---\n\n\n")
				the_file.write("# " + modulename)
				the_file.write("\n\n")
				
				docstring = ast.get_docstring(module)
				
				if docstring:
					the_file.write(docstring)
				
		index += 1
			

		
generate("nodes")
