import csv


def rows(filename):
	output = []
	
	with open(filename) as the_data:
		reader = csv.DictReader(the_data, delimiter=',', quotechar='"', skipinitialspace=True)
		
		for row in reader:
			output.append(row)
			
	return output
		
