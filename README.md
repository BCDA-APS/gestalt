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
can be taken from a comma separated file to provide the widgets with 
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
widgets.

```yaml

UI_Header: !group
    geometry: 100x20
    
    children:
        - !caLabel
            geometry: 0x0 x 40x20
            text: "Port"
            
        - !caLabel
            geometry: 60x0 x 40x20
            text: "RBV"
```


Finally, csv files can be used to provide data for the Widgets. The Spreadsheet.rows() 
function takes in a filename and parses it to provide a set of dictionaries, one for 
each row. The first row is excluded from this as it is used to provide parameter names for 
each column. So if your first row is:

`X,       Y,      COLOR`

Spreadsheet.rows() Will parse each subsequent row and provide a dictionary with 'X', 'Y', 
and 'COLOR' values. These can either individually be accessed and processed to provide
specific configuration of a widget, or alternately, the addChild function optionally takes 
in a  'macros' parameter which will apply the python string formatting function onto the
properties of the widget being added and any children that it contains. Note: this currently
only applies to String datatypes, so it's useful for setting pv channel names, label text,
and some other purposes, but changing positioning, sizing, or coloring will have to be done 
manually. 


Combining everything together you could have a csv file:

```csv
Label,       PV
Port,        Port
Temperature, Temp 
Val,         RBV

```

and a yaml file like:

```yaml
UI_Row: !group
    geometry: 200x25
    
    children:
        - !caLabel
            geometry: 0x0 x 100x20
            text: "{Label}"
            
        - !caLineEdit
            geometry: 100x0 x 100x20
            channel: "$(P)$(R){PV}
```

which is then used in the python with:

```python
    styles = Stylesheet.parse("layout.yml")
    
    a_display = Gestalt.Display(layout=styles["base_window"])
    
    y_val = 0
    
    for row in Spreadsheet.rows("the_data.csv"):
        a_display.addChild( styles["UI_Row"].position(0, y_val), macros=row)
        
        y_val += 25
                
```

And then, to write out the ui file, call the 'writeQt' method

`a_display.writeQt("example.ui")`
