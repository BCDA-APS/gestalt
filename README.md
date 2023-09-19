**G** enerating  
**E** PICS  
**S** creens  
**T** hrough  
**A** ssembling  
**L** ayout  
**T** emplates  



Gestalt is a python application to help make it easy to programmatically 
generate caQtDM '.ui' files from user data. Widgets can be created and 
properties modified without needing to load any Qt libraries, default 
widget parameters can be provided in a YAML stylesheet, and then data 
can be taken from a separate YAML file to provide the widgets with 
with individualized setup.

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


## Creating Your Own Templates

The templates included are not much, so you will likely eventually want
to add your own template into Gestalt to generate new files of your own 
styling.

Creating a new template only requires you to add a new folder into the
templates directory containing three files. Those files are:

* An '\_\_init\_\_.py' file that tells Gestalt what information to display
about your template.

* A 'thumbnail.png' file to give a visual representation of what a
generated file might look like.

* And a 'layout.yml' file which describes the actual templating of the
screen to generate.


### \_\_init\_\_.py

On loadup, Gestalt automatically runs through the folders in the
templates directory and runs the init files found within. These
files only need to contain a single call to the registration function
'registry.add'.

```python
    registry.add("Display Name", path=__path__,
        required_inputs=[("Param1", "Desc1"), ("Param2", "Desc2")],
        example="""
            Param1: 'abc'
            Param2: 123
        """)
```

This function takes four parameters. A positional argument which denotes 
the name to use for this template within the drop-down menu, followed
by three keyword arguments. 

'path' provides the path to the given template folder and can always be 
left as the python variable '\_\_path\_\_'. 

'required_inputs' is a list of tuples that will describe to the user the
meaning of the parameters that are required by the template. Each represents
a top level named parameter needed in the yaml data file.

Finally, 'example' is a string demonstrating an example yaml file that could
be used to generate a ui file. Make sure to include all the same parameters
that you listed in 'required_inputs'.


### thumbnail.png

You should provide a thumbnail file that shows a representative sample of what
an outputted screen would look like. For best visibility, the ratio of width to
height should be 3:2. If your screen is likely to be a different ratio, you
should use transparent padding, vertically or horizontally as needed.


### layout.yml

A caQtDM screen to be generated is represented by a yaml file containing
a graph of children Widget objects. Widgets are created by providing them 
with a Qt widget classname and then setting any properties that should be 
different from the Qt standard.

```yaml
   
small_rect_widget: !caGraphics
    geometry: 100x100
    
    fillstyle: caGraphics::filled
    
    background: $000000
```

#### Data Types

Gestalt can automatically infer the data type of certain structures. For example,
in the above snippet, the geometry property is set to '100x100'. This is recognized
as a two element Rect structure defining the width and height of a widget. Any
bare scalar element (no quotes, no special characters) that consists of two numbers
separated by an 'x' will be interpreted in this way. 

Occasionally, parsing might be ambiguous between different data types. In that instance,
you may need to provide an explicit specifier. A primary example of this would be an
enumeration that does not use the double-colon standard.

```yaml

more_screens: !caRelatedDisplay
    stackingMode: !enum Menu
    
```

The full list of explicit data type tags that are currently recognized and their 
implicit parsing are listed here:


* '!bool' - A python boolean value, see yaml specification for implicit resolution
* '!double' - A double value, see yaml specification for implicit resolution
* '!number' - An integer value, see yaml specification for implicit resolution
* '!string' - A string of characters, see yaml specification for implicit resolution

* '!color' - A color value, will recognize a set of hexadecimal digits after a '$'
character. Either '$RRGGBB' or '$RRGGBBAA'

* '!enum' - A menu selection, will recognize a value that contains a double-colon within

* '!geom' - A rectangle geometry, will recognize numbers separated by an 'x' character.
Either 'Width x Height' or 'X x Y x Width x Height'

* '!set' - A grouped enumeration, will recognize multiple enums separated by the '|'
character


#### Base Widgets

All the caQtDM widgets are supported and can be specified as types using yaml's typing
system. Just put an exclamation mark character before the widget's classname to identify
it to the parser.

```yaml
TweakVal: !caTextEntry            
    geometry: 38x142 x 85x24
                
    channel: "$(P)$(M1).TWV"
```

There is also a special widget type to provide parameters to the top-level Form class.
The type is just '!Form' and it is useful for setting the styleSheet for your screen.
Additionally, the Form widget has a special parameter "margins" which takes in a rectangle
geometry specifying the left, top, right, and bottom margins respectively.


#### Macros

Directly specifying values and leaving certain variables up to runtime macros can get
you pretty far, but the whole point of the generation is to get some form of user
input to use in generating the screen. This is where the data file comes in.

The values that are specified in the data yaml file get parsed and sent to the widgets
during screen construction. You can reference these macros within your layout file by
using braces around the macro name in order to pull values out that were input by the 
user.

```yaml
IOC_Link: !caRelatedDisplay
    geometry: 75x0 x 80x30
    
    label: "-{SECTOR}-{TYPE}-{ID}"
```


Note: currently, macros only work within string variables.



#### Groups

Frequently, you'll want to associate multiple widgets together as part of a group.
This has the benefit of putting the widgets together into a caFrame. X and Y values
for the widgets are then measured against the beginning of the frame, making certain
relational calculation much cleaner. You can also set the parameters of the caFrame
itself to generate backgrounds, outlines, or toggle visibility based on PVs.

There are a few different group types, but all of them share the special parameter,
'children'. This parameter is a list (note, not a map/dict) of widgets that belong
to the group. Groups can be nested if need be and a group will automatically expand
its width and height properties to accomodate the total of all widgets within. 


The basic group is just a '!group'. This type does nothing other than provide a
caFrame.


```yaml

UI_Header: !group
    geometry: 0x40 x 0x0
    
    children:
        - !caLabel
            geometry: 0x0 x 40x20
            text: "Port"
            
        - !caLabel
            geometry: 60x0 x 40x20
            text: "RBV"
```

More usefully, are the group types that provide a layout function. There are three of
these: the '!vrepeat', the '!hrepeat', and the '!grid'. These add on two additional
special parameters, 'repeat_over' and 'padding'.

```yaml

UI_Row: !repeat
    repeat_over: "PLUGINS"
    
    geometry: 0x71 x 0x0
    
    padding: 6
    
    children:
        - !caLindeEdit
        geometry: 10x1 x 110x18
        channel: $(P){Instance}:PortName_RBV
        
        - !caRelatedDisplay            
            label: -More
            
            geometry: 865x0 x 60x20
            
            labels: "{Instance}"
            files: "{Displays}"
            args: "{Args}"
```


'repeat_over' links the group to a specific parameter in the data file. That parameter
should be a list of dictionaries. These layout groups will then create a copy of their
children widgets for every dictionary that is in the data file's list. Each dictionary
in the list is used to provide additional macros that only the given copy can access.
Each copy is then arranged based off of which layout is being applied.

A '!vrepeat' will arrange the successive copies in a vertical flow, the '!hrepeat'
arranges them horizontally across the screen, and the '!grid' tiles the children in a
grid pattern. Between each instance of the children widgets, the 'padding' parameter
sets the number of pixels provide as an offset. For the grid layout, 'padding' applies
in both the vertical and the horizontal direction.

The '!grid' group also uses a third parameter 'aspect_ratio' to control the overall
height and width of the layout. The value defaults to 1.0 and is the ratio between
the number of columns to use and the number of rows. This is an idealized ratio, and
the actual numbers will depend on the number of items being repeated over.



#### Positioners

Positioners are a way to define a widget's position or size that is in some way dependent 
on the parent widget. There are two types of positioners provided, stretch and center.

Unlike groups or other widgets, Positioners don't actually represent anything in regards to
the resulting file. They do not have any parameters nor properties to set. A positioner
should only have a single element within its definition which is the widget you want to
apply the positioner to (though you can use groups to apply a positioner to a set of
widgets).

```yaml
StretchOut: !hstretch
    UITitle: !caLabel
        geometry: 0x0 x 0x32
                
        text: "Middle"
        alignment: Qt::AlignLeft|Qt::AlignVCenter
```

The stretch Positioners, '!hstretch' and '!vstretch', will set a widget's width or
height, respectively, to the value of parent's width or height. This is only calculated
at the relative timing where the widget is being specified. If you add new widgets to
a screen or a group, they have the potential to expand the parent to a larger size,
leaving a mismatch between the two measurements.

Similarly, the center Positioners, '!hcenter' and 'vcenter', will set a widget's position
in the x or y direction, respectively, so that the center of the widget matches up with
the center of the same axis for the parent widget. Again, the center is calculated at
the point that the Positioner is specified, so you may need to specify it later in the
layout to make sure the parent is at the correct size.


#### Included Files

Unlike standard yaml files, layout files do have the ccapability to include other yml
files to provide reuseability. There are two useful yml files already included with
Gestalt, 'colors.yml' and 'widgets.yml'.

Colors provides a set of named colors that can be used instead of constantly specifying
hex values. The naming convention matches up with the full list of CSS colors, alongside
some specially named ones like 'alarm_red' and 'edit_blue' that match up with frequently
used conventions in MEDM. These colors are specified as aliases, so can be used in
widget properties using the '*' dereference character.

```yaml
UITitle: !caLabel
    geometry: 0x0 x 0x32
    foreground: *white
    background: *header_blue
    borderColor: *black
    borderWidth: 3
    
    text: "Label"
```

Widgets is a set of default values that get used often. These can be applied to widgets
of the correct type with the "<<" insert operator.

```yaml
Form: !Form
    <<: *form_default
    
    margins: 5x5x5x5
```
