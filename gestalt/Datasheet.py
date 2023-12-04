import yaml
import csv


def rows(filename):
	output = []
	
	with open(filename) as the_data:
		reader = csv.DictReader(the_data, delimiter=',', quotechar='"', skipinitialspace=True)
		
		for row in reader:
			output.append(row)
			
	return output
		

def parseYAMLFile(filename):
	with open(filename) as the_file:
		return yaml.safe_load(the_file.read())

def parseYAMLString(data):
	return yaml.safe_load(data)
