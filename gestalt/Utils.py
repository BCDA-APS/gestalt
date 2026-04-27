import re
import copy
from pathlib import Path


include_regex = re.compile(r'^#include\s*(.*)$')

def _process_includes(filename, includes_locations, included_files, collect_content):
	the_data_out = "" if collect_content else []

	with open (filename) as the_file:
		the_data_in = the_file.readlines()

		for line in the_data_in:
			check = include_regex.match(line)
			check_locations = copy.copy(includes_locations)

			current_dir = str(Path(filename).parent)

			if current_dir not in check_locations:
				check_locations.append(current_dir)

			if check:
				include_file = check.group(1).strip()
				include_file_fullpath = ""

				for check_dir in check_locations:
					path = str((Path(check_dir) / include_file).resolve())

					if Path(path).exists():
						include_file_fullpath = path
						break

				if include_file_fullpath == "":
					print( "Include file does not exist in path (" + include_file + ")")
					continue


				if include_file_fullpath not in included_files:
					included_files.append(include_file_fullpath)

					if collect_content:
						the_data_out += _process_includes(include_file_fullpath, includes_locations, included_files, True)
					else:
						the_data_out.extend(_process_includes(include_file_fullpath, includes_locations, included_files, False))
						the_data_out.append(include_file_fullpath)

			elif collect_content:
				the_data_out += line

	return the_data_out


def expand_yaml(filename, includes_locations, included_files):
	return _process_includes(filename, includes_locations, included_files, collect_content=True)


def get_includes(filename, includes_locations, included_files):
	return _process_includes(filename, includes_locations, included_files, collect_content=False)
