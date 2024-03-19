**G** enerating  
**E** PICS  
**S** creens  
**T** hrough  
**A** ssembling  
**L** ayout  
**T** emplates  



Gestalt is a python application to interface with generative UI libraries.


Established templates are combined with structured user data to create a 
series of command calls that will build up a screen, arrange widgets, and set
their properties. Layouts are provided to repeat batches of widgets along
a variety of arrangements with specified macros being mapped to user-given 
inputs.

Currently, caQtDM and CSS-Phoebus are supported.


## Requirements

The following python packages are required in order to run gestalt:

* Python >= 3.6
* lxml
* PyQT5
* phoebusgen


## Using Gestalt

Running the top-level gestalt.py will load up all the existing templates
and provide them for you to use and generate files. When you select an
option from the drop-down menu, it will provide you with a description
of the parameters that a given template needs, an existing example, and
the capability to edit said example in-app.

If you would like to load in an existing file outside of the app, you can
click "Load Existing Data" and select the file you wish to use. You may
then change the data within that file using the editor, as well.

When you are satisfied and wish to generate a screen, press the button at
the bottom of the screen labeled "Write Output File" and choose the location
and name for saving. If everything is correct, you'll see a status message
saying that the file has been generated.


[Full Documentation](https://bcda-aps.github.io/gestalt/)
