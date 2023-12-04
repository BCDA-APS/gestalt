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

