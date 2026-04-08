import os
import re
import copy


include_regex = re.compile(r'^#include\s*(.*)$')

def expand_yaml(filename, includes_locations, included_files):
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
					the_data_out += expand_yaml(include_file_fullpath, includes_locations, included_files)

			else:
				the_data_out += line

	return the_data_out


def get_includes(filename, includes_locations, included_files):
	the_data_out = []

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
					the_data_out.extend(get_includes(include_file_fullpath, includes_locations, included_files))
					the_data_out.append(include_file_fullpath)

	return the_data_out
