G enerating  
E PICS  
S creens  
T hrough  
A ssembling  
L ayout  
T emplates  



Gestalt is a python library to help make it easy to programmatically generate caQtDM '.ui' files
from user data. Widgets can be created and properties modified without needing to load any Qt
libraries, default widget parameters can be provided in a YAML stylesheet, and then data can be
taken from a spreadsheet to position the widgets and provide them with individualized setup.


A screen is represented by a Display object containing a graph of children Widget objects. Widgets
are created by providing them with a Qt widget classname and then setting any properties that 
should be different from the Qt standard.

```
    a_display = Gestalt.Display()
    a_display.setProperty("geometry", Type.Rect("600x400"))

    a_widget = Gestalt.Widget("caGraphics")
    a_widget.setProperty("geometry", Type.Rect("100x100"))
    a_widget.setProperty("fillstyle", Type.Enum("caGraphics::filled"))
    a_widget.position(50, 50)
    
    a_display.addChild(a_widget)
```

For repeated creation of the same style of Widget, multiple properties can be combined into a
named style within a stylesheet. An example stylesheet might look like:

```
base_window:
    geometry: 600x400
    
small_rect:
    geometry: 100x100
    
    fillstyle: caGraphics::filled
    
    background: $000000
```

Which can then be used to construct Displays and Widgets either through the 'layout' parameter
in the constructors, or through the 'setLayout' function.

```
    styles = Stylesheet.parse("layout.yml")
    
    a_display = Gestalt.Display(layout=styles["base_window"])
    
    a_display.addChild( Gestalt.Widget("caGraphics")
                        .setLayout(styles["small_rect"])
                        .position(50, 50) )
                        
```

Finally, spreadsheets can be used to provide data for the Widgets. The Data.rows() and Data.cols()
functions take an excel spreadsheet and parses it to provide a set of data structures, one for each
row or column respectively. The first item is excluded from this as it is used to provide parameter
names for each cell in each row/column. So a first row of:

`X    |   Y   |   COLOR`

Would parse each subsequent row and provide a dictionary with 'X', 'Y', and 'COLOR' values. Combining
that with what we've been doing so far gives us:

```
    styles = Stylesheet.parse("layout.yml")
    
    a_display = Gestalt.Display(layout=styles["base_window"])
    
    for row in Data.rows("the_data.xlsx"):
        a_display.addChild( Gestalt.Widget("caGraphics")
                .setLayout(styles["small_rect"])
                .setProperty("foreground", Type.Color(row["COLOR"]))
                .position(row["X"], row["Y"]) )
                
```

And then, to write out the ui file, call the 'writeQt' method

`a_display.writeQt("example.ui")`
