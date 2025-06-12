import os
import re
import copy
import yaml
import json
import csv
import configparser


def rows(filename):
	output = []
	
	with open(filename) as the_data:
		reader = csv.DictReader(the_data, delimiter=',', quotechar='"', skipinitialspace=True)
		
		for row in reader:
			output.append(row)
			
	return output
		

def parseJSONFile(filename):
	with open(filename) as the_file:
		return json.loads(the_file.read()) or {}
		
def parseJSONString(data):
	return json.loads(data) or {}
	
	
	
include_regex = re.compile(r'^#include\s*(.*)$')

def read_file(filename, includes_locations, included_files):
	the_data_out = ""
	
	with open (filename) as the_file:
		the_data_in = the_file.readlines()
		
		for line in the_data_in:
			check = include_regex.match(line)
			check_locations = copy.copy(includes_locations)
			
			current_dir = os.path.dirname(filename)
			
			if current_dir not in check_locations:
				check_locations.append(os.path.dirname(filename))
			
			if check:
				include_file = check.group(1).strip()
				include_file_fullpath = ""
				
				for check_dir in check_locations:
					path = os.path.abspath(check_dir + "/" + include_file)
						
					if os.path.exists(path):
						include_file_fullpath = path
						break
				
				if include_file_fullpath == "":
					print( "Include file does not exist in path (" + include_file + ")")
					continue
				
				
				if include_file_fullpath not in included_files:
					included_files.append(include_file_fullpath)
					the_data_out += read_file(include_file_fullpath, includes_locations, included_files)
					
			else:
				the_data_out += line
				
	return the_data_out

	
def parseYAMLFile(filename):
	return yaml.safe_load(read_file(filename, [os.path.abspath(os.path.dirname(filename))], []))

def parseYAMLString(data):
	return yaml.safe_load(data) or {}	

	
	
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
					matches = check.strip("{}").split(",")
					
					if matches:	
						temp = {}
						
						for i in range(len(pattern)):
							temp[pattern[i]] = matches[i].strip().strip('"')
							
						output[curr_file].append(temp)
						
			elif check.startswith("}"):
				load_values = False
				
	return output

def parseINIFile(filename):
	output = configparser.ConfigParser()
	output.read(filename)
	return output
