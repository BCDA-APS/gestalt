---
layout: default
title: Nodes
parent: Reference
nav_order: 1
has_toc: false
---

# Nodes
{: .no_toc}


## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}



## About

There are four major categories of Nodes: Widgets, Logical Groups, Layouts, and 
Positioners. Nodes contain a set of attribute data describing their configuration and 
the logic of how to apply those attributes to a given output data format.


## Widgets

Widget nodes are the representations of individual widgets within each UI tool that
gestalt outputs to. There are a variety of output-independent widgets defined for
use which can be referenced here. These nodes will be automatically matched up to
the equivalent widget in CSS-Phoebus or caQtDM or pyDM when writing the output file.
Care has been taken to attempt to match up visuals and behavior so that generated screens 
will be near identical between UI tools.

As well, there is support for directly interfacing with widgets for a specific tool.
Directly using the widget name of a specific caQtDM or CSS widget will allow you to
set attributes with names and values equivalent to the names and values within their
equivalent designer programs (caQtDM or phoebusgen). 

### CSS Widget

---

The list of recognized CSS Widgets is as follows: "ActionButton", "Array", "BooleanButton", 
"CheckBox", "ComboBox", "DataBrowser", "EmbeddedDisplay", "FileSelector", "LEDMultiState", 
"Label", "Meter", "NavigationTabs", "Picture", "ProgressBar", "RadioButton", "ScaledSlider", 
"Scrollbar", "SlideButton", "Spinner", "StripChart", "Symbol", "Table", "Tabs", "Tank", 
"TextSymbol", "TextUpdate", "Thermometer", "ThreeDViewer", "WebBrowser", and "XYPlot".

Attributes are set using the name of the function used by phoebusgen. For example, a label's `Auto Size`
field in CSS-Phoebus would be set with the `auto_size` attribute in Gestalt.


* **Special Attributes**

|    Name   |  Type  | Description|
|-----------|--------|------------|
| geometry  | Rect   | A rectangle describig the position and dimensions of the widget |


* **Example**

```yaml
- !Label
    geometry: 5x0 x 120x20
    
    text: "Label {N}"
    transparent: false
    background: *header_blue
    foreground: Attention
    font: -Liberation Sans - bold - 12
```

### caQtDM Widget

---

The list of recognized caQtDM Widgets is as follows: "caLabel", "caLineEdit", "caTextEntry", 
"caMenu", "caRelatedDisplay", "caNumeric", "caApplyNumeric", "caSlider", "caChoice", "caTextEntry",
"caMessageButton", "caToggleButton", "caSpinbox", "caByteController", "caLabelVertical", 
"caGraphics", "caPolyLine", "caImage", "caInclude", "caDoubleTabWidget", "caClock", "caLed", 
"caLinearGauge", "caMeter", "caCircularGauge", "caMultiLineString", "caThermo", "caCartesianPlot",
"caStripPlot", "caByte", "caTable", "caWaveTable", "caBitnames", "caCamera", "caCalc", 
"caWaterfallPlot", "caScan2D", "caLineDraw", "caShellCommand", "caScriptButton", "caMimeDisplay".

Attributes are set with the same names used for the widget's Qt properties.


* **Special Attributes**

caQtDM widgets don't have any special attributes.


* **Example**

```yaml
- !caMessageButton
    background: *edit_blue
    colorMode: caMessageButton::Static
    
    geometry: 126x140 x 24x24
    pressMessage: "1"
    channel: "$(P)$(M{N}).TWF"
    label: ">"
```

### Form

---

A special widget used to set values for the top-level window.


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| margins    | Rect   | A set of numbers describing the number of pixels to leave clear on the left, top, right, and bottom of the window respectively |
| background | Color  | The background color for the Form, $BBBBBB by default |
| title      | String | The display name in the header bar of the window |


* **Example**  

```yaml
Form: !Form
    background: $123456
    margins: 5x5x5x5
```


## Logical Groups

Logical groups perform some form of calculation upon their children widgets. This includes
the '!conditional' type as well as the Template system and Apply type. 

A conditional group uses a boolean value to decide whether to add their contents to the screen 
or not. Within the template file, a conditional group will have the 'condition' attribute 
specified as the name of a macro within the data file.

If the macro's value is equivalent to a false value, then none of the group's contents
are included in the resulting UI screen. Otherwise, the conditional is treated like a
basic group.

The Template and Apply system saves sets of Nodes to later be included in other definitions
while being able to define certain attributes with macros.


## Layouts

Layout nodes take a group of widgets and automatically position them, so that specific
x and y values don't need to be provided to each element. The layouts available to use
are Flows, Repeats, and the Grid.

* Flows arrange items along a given axis, placing each successive widget right after the
next one.

* Repeats will copy their children widgets as a group and repeat them along a given axis,
using a set of macros to configure each repeated line according to the user's input.

* Grids work like the Repeat node, but will copy the widgets according to
a grid pattern, using a specified ratio to determine the number of columns and rows.


## Positioners


Positioners are special tags that can be applied to a widget type which overwrite the
geometry of the given widget when the output file is written. All other attributes of
the widget are defined as normal and not touched by the positioner.

When defining the widget you want to position, just prepend with widget's type with the
positioner's type. So if you have a Text widget, which is normally indicated with the '!Text'
type, and you want to horizontally center it within its parent, you would change that type
to '!hcenter:Text'.

Positioners are set up to be generated last among a set of unordered children nodes. This allows 
the rest of the nodes to expand the size of a parent widget before determining positioning. Be
careful though, as this does mean that the later generated widgets will appear above any other
widgets they share area with, despite being written in the stylesheet earlier. You can overwrite
this behavior by setting the "render-order" attribute to 0, but you may then have to define your
positioner node in a later part of the stylesheet in order for it to see the correct parent height
and width.

As well, it's important to note that this is only for unordered sets of children nodes. FlowNodes
will ignore this order and will place children nodes in the order they are defined in the template.

