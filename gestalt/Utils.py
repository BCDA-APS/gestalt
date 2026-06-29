import re
import copy
from pathlib import Path
from collections import namedtuple


include_regex = re.compile(r'^#include\s*(.*)$')

SourceLocation = namedtuple("SourceLocation", ["file", "line"])
SourceLocation.__str__ = lambda self: "{}:{}".format(self.file, self.line)

# Source map: maps expanded line numbers to (filename, original_line) tuples.
# Built during expand_yaml, used by resolve_location.
source_map = []


def resolve_location(mark):
	"""Resolve a YAML Mark's expanded line number to the original file and line.
	
	Args:
		mark: A YAML Mark object with a `line` attribute, or a SourceLocation.
	
	Returns:
		A SourceLocation(file, line) namedtuple, or None if the mark cannot be resolved.
	"""
	if mark is None:
		return None
	
	if isinstance(mark, SourceLocation):
		return mark
	
	line = getattr(mark, "line", None)
	
	if line is not None and line < len(source_map):
		return source_map[line]
	
	return None


def _process_includes(filename, includes_locations, included_files, collect_content):
	the_data_out = "" if collect_content else []
	short_name = Path(filename).name

	with open (filename) as the_file:
		the_data_in = the_file.readlines()

		for line_num, line in enumerate(the_data_in, start=1):
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
					searched = ", ".join(check_locations)
					raise FileNotFoundError(
						"Include file not found: '{}' (searched: {})".format(
							include_file, searched))


				if include_file_fullpath not in included_files:
					included_files.append(include_file_fullpath)

					if collect_content:
						the_data_out += _process_includes(include_file_fullpath, includes_locations, included_files, True)
					else:
						the_data_out.extend(_process_includes(include_file_fullpath, includes_locations, included_files, False))
						the_data_out.append(include_file_fullpath)

			elif collect_content:
				source_map.append(SourceLocation(short_name, line_num))
				the_data_out += line

	return the_data_out


def expand_yaml(filename, includes_locations, included_files):
	source_map.clear()
	return _process_includes(filename, includes_locations, included_files, collect_content=True)


def get_includes(filename, includes_locations, included_files):
	return _process_includes(filename, includes_locations, included_files, collect_content=False)
