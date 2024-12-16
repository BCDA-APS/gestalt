---
layout: default
title: Using the Command Line
nav_order: 3
---

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}



## Command Line

Gestalt has a number of command line options to be able to generate screens beyond just
the built-in templates. As well, users are able to provide input data in a variety of 
formats beyond just YAML. 

The structure of calling Gestalt on the command line is:

> gestalt.py [OPTIONS] [TEMPLATE]


## Options


### -i, --input

Input data to apply to the template file. Either a string containing data in a yaml 
format, or the path to a file to be parsed according to the input format.


### -f, -r, --from, --read

Specifies which file parser should be used to read an input data file to generate the macros
that will be fed to the template file. By default, Gestalt will attempt to determine the
parser automatically based on the file suffix of the input file.

Recognized values for file parser are:

* **yml**, **yaml** - Input file is a YAML file
* **json**, **JSON** - Input file is a JSON file
* **substitutions**, **msi** - Input file is an EPICS substitutions file. Individual substitution
lines are converted to dictionaries with keys based upon the specified pattern. Substitutions are
arranged into lists, which are linked with the name of the database file being substituted.
* **ini**, **cfg** - Input file is an INI-style file.
* **string**, *str** - Instead of an input file, read the input string as a yaml string.


### -o, --output

Filepath for the output UI name. By default, if an output format is specified, this will be 
generated based off of the template file name and the output format. If an output format is
not specified, then you must specify an output filename.


### -t, -w, --to, --write

Specifies the output UI file format to write. By default, if an output filepath is specified,
Gestalt will attempt to determine what file format to output based upon the file suffix of the
output filename. If no output file path is specified, then you must specify which output format
to write.

Recognized values for file writer are:

* **qt**, **ui** - Output file is for caQtDM  
* **css**, **bob** - Output file is for CSS-Phoebus  


### --include

Additional folder to include in your search path for template files that may be included using
'#include' statements. This option can be applied multiple times, each time specifying a new
folder to append to the search path. By default, Gestalt's widgets folder is already included 
in the search path (for widgets.yml and colors.yml).


