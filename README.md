**G** enerating  
**E** PICS  
**S** creens  
**T** hrough  
**A** ssembling  
**L** ayout  
**T** emplates  



Gestalt is a python library to help make it easy to programmatically 
generate caQtDM '.ui' files from user data. Widgets can be created and 
properties modified without needing to load any Qt libraries, default 
widget parameters can be provided in a YAML stylesheet, and then data 
can be taken from a separate YAML file to provide the widgets with 
with individualized setup.

For a full example, see: https://github.com/keenanlang/gestalt_example

## Using Gestalt

A caQtDM screen to be generated is represented in the code by a Display 
object containing a graph of children Widget objects. Widgets are created 
by providing them with a Qt widget classname and then setting any properties 
that should be different from the Qt standard.

```python
    a_display = Gestalt.Display()
    a_display.setProperty("geometry", Type.Rect("600x400"))

    a_widget = Gestalt.Widget("caGraphics")
    a_widget.setProperty("geometry", Type.Rect("100x100"))
    a_widget.setProperty("fillstyle", Type.Enum("caGraphics::filled"))
    a_widget.position(50, 50)
    
    a_display.addChild(a_widget)
```

For repeated creation of the same style of Widget, multiple properties can 
be combined into a named style within a stylesheet. An example stylesheet 
might look like:

```yaml
base_window:
    geometry: 600x400
    
small_rect:
    geometry: 100x100
    
    fillstyle: caGraphics::filled
    
    background: $000000
```

Which can then be used to construct Displays and Widgets either through the 
'layout' parameter in the constructors, or through the 'setProperties' function.

```python
    styles = Stylesheet.parse("layout.yml")
    
    a_display = Gestalt.Display(layout=styles["base_window"])
    
    a_display.addChild( Gestalt.Widget("caGraphics")
                        .setProperties(styles["small_rect"])
                        .position(50, 50) )
                        
```

Widgets can also be constructed within the stylesheet itself. Just tag the layout
data with the widget classname you want to construct.

```yaml
   
small_rect_widget: !caGraphics
    geometry: 100x100
    
    fillstyle: caGraphics::filled
    
    background $000000
```

This generates a Gestalt.Widget instance, which can be added to a display just like
the ones you construct in code.

```python
    styles = Stylesheet.parse("layout.yml")
    
    a_display = Gestalt.Display(layout=styles["base_window"])
    
    a_display.addChild( styles["small_rect_widget"].position(50, 50) )
    
```

While individually constructing and adding widgets to your display using yaml doesn't
save you much effort, you can group widgets together into a single caFrame that can
be added with a single addChild command. As well, X and Y coordinates of widgets within 
the group are calculated offset from the position of the frame, which can frequently
make calculations cleaner.

A group object looks for a specific "children" tag in its mapping and expects to find
a list of widgets. Those widgets will automatically be put in as a caFrame's children
widgets. While you can set the width and height for a group object, the default behavior
will expand the geometry to accomodate any child widget that it contained within.

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


Additionally, you can have a repeater object, which will generate a copy of every one
of its child widgets for each index of a provided list. The special tag "repeat_over"
can be set to the name of a key in a data file that will contain a list of items. For
each item in that list, it will be passed off to the widget copies to be used as a 
macro list.

There are two types of repeaters, vertical and horizontal, indicating the direction in
which copies of the given widgets will be offset. Another special key, "padding" gives
the number of extra pixels to offset those copies beyond just touching as close as 
possible. Horizontal repeaters are created with the !hrepeat class, while vertical
repeaters can be created with either !vrepeat or just !repeat.

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
        


Finally, yaml files can also be used to provide data for the Widgets. The Datasheet.parseFile()
and Datasheet.parseString() functions takes in a filename or a string containing yaml data
respectively, and parses it to provide a data structure that can be used in construction.


Largely, all of this can be left behind the scenes and the Gestalt.generateQtFile() function
can be used. This automates a lot of the above steps. It takes in the named argument, stylesheet,
parses it into the template stylesheet. Then, either datafile or datastr will be parsed with
Datasheet.parseFile or Datasheet.parseString respectively to generate a macro dictionary. Each
top-level widget in the template stylesheet is added to a QtDisplay and then the data macros
are fed to the resulting structure to write out the qt file. With the parameter, outputfile 
providing the location where to write the file.
