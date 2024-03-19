---
layout: default
title: Widgets
parent: Nodes
nav_order: 1
---

# Widgets
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

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


## Output-Independent Widgets

### Arc

---

A basic rectangle shape that can either be filled or an outline

Angles are defined in relation to the positive x axis. With 0 degrees
following that axis, and angles proceeding in the counter-clockwise
direction.

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| background   | Color  | Widget interior color, transparent by default |
| border-color | Color  | Widget outline color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| start-angle  | Number | Angle of the starting ray of the arc, 0 by default |
| span         | Number | Degrees that the arc covers, 90 by default |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
SimpleBox: !Arc
    geometry: 100x100
    border-width: 5
    
    start-angle: 45
    span: 180
```

<br>

### ByteMonitor

---

A widget displaying the individual bits of a pv value

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| pv         | String | The PV whose bits to display |
| start-bit  | Number | The initial bit offset for the first bit being displayed, 0 by default |
| bits       | Number | The number of bits to display, increments from the start-bit, defaults to displaying till the end of the word |
| off-color  | Color  | The display color for a bit being 0, $3C643C by default |
| on-color   | Color  | The display color for a bit being 1, $00FF00 by default |
| horizontal | Bool   | Whether to arrange the display horizontally, defaults to True |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
StatusBits: !ByteMonitor
    geometry: 165x12
    
    pv: "$(P)m1.MSTA"
    bits: 15
```

<br>

### ChoiceButton

---

A widget representing a set of buttons that gets its options from an enumerable pv

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| selected   | Color  | Selected item color, defaults to background color |
| font       | Font   | Widget display font |
| pv         | String | The PV containing the enumerable value |
| horizontal | Bool   | Whether to arrange the buttons horizontally, defaults to True |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
OnOff: !ChoiceButton
    geometry: 215x20
    
    pv: "$(P)userCalcEnable.VAL"
    foreground: *black
    background: *edit_blue
```

<br>

### Ellipse

---

A basic ellipse shape that can either be filled or an outline

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| background   | Color  | Widget interior color, transparent by default |
| border-color | Color  | Widget outline color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
SimpleBox: !Ellipse
    geometry: 100x100
    border-width: 5
```

<br>

### Form

---

A special widget used to set values for the top-level window.


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| margins    | Rect   | A set of numbers describing the number of pixels to leave clear on the left, top, right, and bottom of the window respectively |
| background | Color  | The background color for the Form, $BBBBBB by default |


* **Example**  

```yaml
Form: !Form
    background: $123456
    margins: 5x5x5x5
```

<br>

### Image

---

A widget that displays a given image file


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| file       | String | The filepath of the image to display |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
ComplicatedStructure: !Image
    file: "/path/to/image/Beamline.png"
```

<br>

### LED

---

A widget that changes color based upon the value of a given pv. Has one of three states,
true, false, or undefined based upon a match with values given by the widget.


* **Special Attributes**

|       Name      |    Type   | Description|
|-----------------|-----------|------------|
| geometry        | Rect      | A rectangle describing the position and dimensions of the widget |
| square          | Bool      | Change widget shape to rectangular rather than circular |
| false-value     | Number    | Set widget to false-color when pv value equals false-value, 0 by default |
| true-value      | Number    | Set widget to true-color when pv value equals true-value, 1 by default |
| false-color     | Color     | The display color for a false value, $3C643C by default |
| true-color      | Color     | The display color for a true value, $00FF00 by default |
| undefined-color | Color     | The display color for any other value, $A0A0A4 by default |
| border-color    | Color     | Widget border color, $000000 by default |
| pv              | String    | The PV to read data from |
| visibility      | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
OnOff_Readback: !LED
    pv: "$(P)userCalcEnable.VAL"
    
    geometry: 24x24
    square: true
```

<br>

### Menu

---

A widget representing a menu that gets its options from an enumerable pv


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| pv         | String | The PV containing the enumerable value |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Menu
    foreground: *black
    background: *edit_blue
    geometry: 355x0 x 80x20
    pv: $(P){Instance}:EnableCallbacks
```

<br>

### MessageButton

---

A widget representing a button that writes a value to a pv when pressed

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| pv         | String | The PV that will be written to |
| value      | String | The value to write to the PV |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !MessageButton
    foreground: *black
    background: *edit_blue

    text: "Write Value"
    
    geometry: 10x200 x 100x20
    
    pv: "xxx:yyy:zzz"
    value: 1
```

<br>

### Polygon

---

A closed shape consisting of a set of points that can either be filled or an outline


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| background   | Color  | Widget interior color, transparent by default |
| border-color | Color  | Widget outline color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| points       | List   | A list of Rect's representing the vertices of the polygon |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
SimpleBox: !Polygon
    geometry: 100x100
    border-width: 5
    
    points: [ 10x10, 90x10, 90x90, 10x90 ]
```

<br>

### Polyline

---

A set of contiguous line segments


* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| border-color | Color  | Widget line color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| points       | List   | A list of Rect's representing the contiguous points of the polyline |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
Star: !PolyLine
    geometry: 40x40
    points: [ 20x0, 0x40, 40x10, 0x10, 40x40, 20x0 ]
```

<br>

### Rectangle

---

A basic rectangle shape that can either be filled or an outline

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| geometry     | Rect   | A rectangle describing the position and dimensions of the widget |
| background   | Color  | Widget interior color, transparent by default |
| border-color | Color  | Widget outline color, $000000 by default |
| border-width | Number | Thickness of widget outline, 2 by default |
| visibility   | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
SimpleBox: !Rectangle
    geometry: 100x100
    border-width: 5
```

<br>

### RelatedDisplay

---

A widget representing a menu of other UI screens that can be opened by a user.

These other screens are detailed by the attribute `links` which is a list of
dictionaries. Within each dictionary, the following values can be defined:

* label  - The display name for the screen to open
* file   - The filepath for the screen to open
* macros - Any macros to pass the screen when opening
* replace - Optional, Whether to replace the parent screen when opening, False by default

<br>

* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| links      | List   | A list of dictionaries describing the linked UI screens |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !RelatedDisplay
    foreground: *black
    background: *edit_blue

    text: "Open xxx"
    
    geometry: 10x200 x 100x20

    links:
        - { label: "File 1", file: "xxx.ui", macros: "P=1,R=A" }
```

<br>

### Scale

---

A widget representing a bar filling up based on a pv's value versus its limits


* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| background   | Color     | Color of the unfilled portion of bar, $C9C9C9 by default |
| foreground   | Color     | Color of the filled portion of bar, $0000FF by default |
| horizontal   | Bool      | Whether to align the bar horizontally, defaults to False |
| pv           | String    | The PV being monitored |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Scale
    geometry: 0x0 x 50x200
    foreground: *burlywood
    pv: "xxx:yyy:zzz"
```

<br>

### ShellCommand

---

A button that will trigger the running of a selected shell command

These shell commands are detailed by the attribute `commands` which is a list of
dictionaries. Within each dictionary, the following values can be defined:

* label   - The display name for the command to run
* command - The command and all arguments that will be executed

<br>


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| commands   | List   | A list of dictionaries describing the commands that can be run |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
ExampleCommand: !ShellCommand
    geometry: 10x10 x 80x20
    
    text: "Say"
    
    commands: 
        - { label: "Hello",   command: "echo 'Hello'"  }
        - { label: "Goodbye", command: "echo 'Goodbye'"}
```

<br>

### Slider

---

A widget that uses a slider to control output to a pv

* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| horizontal | Bool   | Whether to arrange the display horizontally, defaults to True |
| pv           | String    | The PV being monitored |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Slider
    geometry: 140x0 x 120x20
    pv: "$(P)Ao10"
```

<br>

### Text

---

A widget representing a basic text label.


* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| text         | String    | The widget's display text |
| foreground   | Color     | Widget foreground color |
| background   | Color     | Widget background color |
| border-color | Color     | Widget border color |
| border-width | Number    | Widget border thickness in pixels |
| font         | Font      | Widget display font |
| alignment    | Alignment | Display text alignment. |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !Text
    geometry: 5x0 x 120x20
    
    text: "Label Text"
    font: -Liberation Sans - bold - 12
    
    alignment:
        horizontal: Center
        vertical: Center
```

<br>

### TextEntry

---

A widget representing a text entry field.

* **Special Attributes**

|    Name    |    Type   | Description|
|------------|-----------|------------|
| geometry   | Rect      | A rectangle describing the position and dimensions of the widget |
| foreground | Color     | Widget foreground color |
| background | Color     | Widget background color |
| font       | Font      | Widget display font |
| alignment  | Alignment | Display text alignment. |
| pv         | String    | The PV that will be written to |
| visibility | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !TextEntry
    geometry: 5x0 x 120x20
    
    pv: "$(P)$(R)Description"
    
    alignment: BottomLeft
```

<br>

### TextMonitor

---

A widget representing a text display field

* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| foreground   | Color     | Widget foreground color |
| background   | Color     | Widget background color |
| border-color | Color     | Widget border color |
| border-width | Number    | Widget border thickness in pixels |
| font         | Font      | Widget display font |
| alignment    | Alignment | Display text alignment. |
| pv           | String    | The PV to read data from |
| visibility   | String    | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
- !TextMonitor
    geometry: 5x0 x 120x20
    
    pv: "$(P)$(R)Description_RBV"
    
    alignment: CenterRight
```
