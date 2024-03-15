import re
import yaml
import json
import csv


def rows(filename):
	output = []
	
	with open(filename) as the_data:
		reader = csv.DictReader(the_data, delimiter=',', quotechar='"', skipinitialspace=True)
		
		for row in reader:
			output.append(row)
			
	return output
		

def parseJSONFile(filename):
	with open(filename) as the_file:
		return json.loads(the_file.read())
		
def parseJSONString(data):
	return json.loads(data)
	
def parseYAMLFile(filename):
	with open(filename) as the_file:
		return yaml.safe_load(the_file.read())

def parseYAMLString(data):
	return yaml.safe_load(data)

def parseSubstitutionFile(filename):
	output = {}
	
	curr_file = ""
	pattern = []
	pattern_next = False
	load_values = False
	
	pattern_line = re.compile(r"(\S+)\s*")
	
	with open(filename) as the_file:
		for line in the_file:
			check = line.strip()
			
			if check.startswith("file"):
				curr_file = str.split(check, " ")[1].strip('"')
				output[curr_file] = []
			
			elif check.startswith("pattern"):
				pattern_next = True
				
			elif check.startswith("{"):
				if pattern_next:
					matches = pattern_line.findall(check.strip("{}"))
					
					if matches:
						pattern = matches
						
					pattern_next = False
					load_values = True
					
				elif load_values == True:
					matches = pattern_line.findall(check.strip("{}"))
					
					if matches:						
						temp = {}
						
						for i in range(len(pattern)):
							temp[pattern[i]] = matches[i].strip('",')
							
						output[curr_file].append(temp)
						
			elif check.startswith("}"):
				load_values = False
				
	return output
