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

* And at least a single yml file which describes the actual templating of the
screen to generate.


### \_\_init\_\_.py

On loadup, Gestalt automatically runs through the folders in the
templates directory and runs the init files found within. These
files only need to contain a single call to the registration function
'registry.add'.

```python
    registry.add("Display Name", path=__path__,
        qt_stylesheet= "layout.yml",
        required_inputs=[("Param1", "Desc1"), ("Param2", "Desc2")],
        example="""
            Param1: 'abc'
            Param2: 123
        """)
```

This function takes up to six parameters. A positional argument which 
denotes the name to use for this template within the drop-down menu, 
followed by a set of keyword arguments. 

'path' provides the path to the given template folder and can always be 
left as the python variable '\_\_path\_\_'. 

'qt_stylesheet' and/or 'css_stylesheet' tells gestalt which file to use
as the stylesheet for given conversion type.

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

A screen to be generated is represented by a yaml file containing a graph 
of children Widget objects. Widgets are created by providing them with a 
Qt or CSS widget classname and then setting any properties that should be 
different from the Qt standard.

```yaml
   
small_rect_widget: !caGraphics
    geometry: 100x100
    
    fillstyle: caGraphics::filled
    
    background: $000000
```

```yaml

small_rect_widget: !Rectangle
    geometry: 100x100
    
    line_color: $000000
    background_color: $000000

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

* '!font' - A Font specification, will recognize a dash followed by a font name.
Optionally, extra dashes can also specify font style and size. '-DejaVu Sans Mono - regular - 16'

* '!enum' - A menu selection, will recognize a value that contains a double-colon within

* '!geom' - A rectangle geometry, will recognize numbers separated by an 'x' character.
Either 'Width x Height' or 'X x Y x Width x Height'

* '!set' - A grouped enumeration, will recognize multiple enums separated by the '|'
character


#### Base Widgets

All the caQtDM and CSS-Phoebus widgets are supported and can be specified as types using 
yaml's typing system. Just put an exclamation mark character before the widget's classname 
to identify it to the parser.

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

The basic group is just a '!group', which provides a caFrame when used within a
caQtDM template, and Group widget when used within a CSS template.


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

In addition to the 'children' attribute, all groups also have the additional attribute
'margins'. This specifies a number of pixels to keep clear along the various sides of
the group. Margins are specified with a !geom type, with the x, y, width, and height
values corresponding to the left, top, right, and bottom margins respectively.

```yaml
UI_Header: !group
    geometry: 0x40 x 0x0
    margins: 5x0x5x0
    
    children:
        - !caLabel
            geometry: 0x0 x 40x20
            text: "Port"
            
        - !caLabel
            geometry: 60x0 x 40x20
            text: "RBV"

```

Elements within the group have their X and Y coordinates shifted according to the left
and top margins. And if that would extend the widget's area into the group's right or
bottom margin, the group's width or height is then adjusted accordingly.


Aside from providing some structure to the resulting file, a basic group isn't all that 
helpful. More usefully, are the group types that provide logical or layout functions.


#### Logical Groups

Logical groups perform some form of calculation upon their children widgets. Currently,
the only logical group used is the '!conditional' type. A conditional group uses a 
boolean value to decide whether to add their contents to the screen or not. Within the
template file, a conditional group will have the 'condition' attribute specified as the
name of a macro within the data file.

If the macro's value is equivalent to a false value, then none of the group's contents
are included in the resulting UI screen. Otherwise, the conditional is treated like a
basic group.


#### Layout Groups

Layout groups take a group of widgets and automatically position them, so that specific
x and y values don't need to be provided to each element. The basic layout group type
is the '!flow'. A flow arranges successive widgets in a list, one after another, in a 
single direction. 

```yaml
NumberedLED: !flow
    children:
        - !caLabel
            font: -Sans Serif - Regular - 8
            
            geometry: 50x15
            
            alignment: Qt::AlignHCenter|Qt::AlignVCenter
            fontScaleMode: ESimpleLabel::None
            
            text: "Input 1"
        
        - !caLed
            channel: !string "$(P)Bi1.VAL"
            trueColor: *alarm_red
            falseColor: *alarm_green
            
            borderColor: *transparent
            
            gradientEnabled: false
            
            geometry: 22x22

```

By default, a '!flow' will arrange items along a vertical axis. This can be made
explicit by using the '!vflow' type, or can be made to use a horizontal axis with
the '!hflow' type.

The flow type also introduces a new attribute 'padding' which is used in all successive
groups. Padding is the number of pixels to space out each successive element in the
flow. 

```yaml
CIO_Title: !hflow
    geometry: 0x2 x 0x0
    padding: 5
    
    children:                            
        - !caLabel
            geometry: 70x20
            text: "CIO 0-3"
            
        - !caLineEdit
            geometry: 80x20
            background: *edit_blue
            foreground: *black
            colorMode: caLineEdit::Static
            
            channel: !string "$(P)CIOIn"
            
        - !caLabel
            geometry: 90x20
            text: "MIO 0-2"
            
        - !caLineEdit
            geometry: 80x20
            background: *edit_blue
            foreground: *black
            colorMode: caLineEdit::Static
            
            channel: !string "$(P)MIOIn"
```

Flows are good for setting up basic formatting, but you are still having to specify
every element that goes into a screen. Frequently, you will have multiples of the
exact same group of widgets, just with changes in the text of labels or in the PV's 
to connect to. For this, there is an extension of the flow group, which is the 
'!repeat' type. 

A repeat group has another new attribute, 'repeat_over', which links the group to a
specific parameter in the data. That parameter should either be a number or a list of 
dictionaries.

```yaml

UI_Row: !repeat
    repeat_over: "PLUGINS"
    
    geometry: 0x71 x 0x0
    
    padding: 6
    
    children:
        - !caLineEdit
            geometry: 10x1 x 110x18
            channel: $(P){Instance}:PortName_RBV
        
        - !caRelatedDisplay            
            label: -More
            
            geometry: 865x0 x 60x20
            
            labels: "{Instance}"
            files: "{Displays}"
            args: "{Args}"
```


The repeat iterates over the given parameter, generates a copy of all its children
widgets, applies a set of macros to the group, and then positions the entire group
of widgets according to either a horizontal or vertical flow. The default flow is
vertical, and can be specified or switch by using the '!vrepeat' or '!hrepeat' types.

The macros that get applied to the widgets are based upon the type of the parameter
that is listed in the repeat_over attribute. If the user specifies a single number,
that represents the number of iterations that the repeat will loop. Starting at zero,
the loop will increment up to "VALUE - 1". On each loop, the macro 'N' will
be set to the current value and provided to the widgets generated in that loop. The
current loop index is also always available in the macro '__index__', regardless of 
the data type used for repeat_over.

If the specified parameter is instead a list of dictionaries, then the dictionaries
will be treated as the macros to supply the widgets. The loop will iterate over each
of the specified mappings and will provide the children elements of the group with
those macros (alongside the macros in the data file).


The final group is the '!grid' which tiles children in grid pattern. In this type,
the padding parameter specifies the padding between groups in both the vertical as
well as the horizontal direction.

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
#include colors.yml

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
