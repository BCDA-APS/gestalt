#! /usr/bin/env python3

import os
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
		
		with open(output_path, "w") as the_file:
			the_file.write("{% include header.md " + info + " %}\n")
			the_file.flush()
			os.system("pydoc-markdown -m " + modulename + " --search-path ../gestalt/" + package + " >> " + output_path)
			
		index += 1
			

		
generate("nodes")
