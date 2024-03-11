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

The list of recognized CSS Widgets is as follows: "ActionButton", "Arc", "Array", "BooleanButton", 
"ByteMonitor", "CheckBox", "ComboBox", "DataBrowser", "Ellipse", "EmbeddedDisplay", 
"FileSelector", "Image", "LEDMultiState", "Label", "Meter", "NavigationTabs", 
"Picture", "Polygon", "Polyline", "ProgressBar", "RadioButton", "Rectangle", "ScaledSlider", 
"Scrollbar", "SlideButton", "Spinner", "StripChart", "Symbol", "Table", "Tabs", "Tank", "TextEntry", 
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


* **Example**

```yaml
StatusBits: !ByteMonitor
    geometry: 165x12
    
    pv: "$(P)m1.MSTA"
    bits: 15
```


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
| horizontal | Bool   | Whether to arrange the buttons horizontally, defaults to False |


* **Example**

```yaml
OnOff: !ChoiceButton
    geometry: 215x20
    
    pv: "$(P)userCalcEnable.VAL"
    foreground: *black
    background: *edit_blue
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


* **Example**  

```yaml
Form: !Form
    background: $123456
    margins: 5x5x5x5
```


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


* **Example**

```yaml
OnOff_Readback: !LED
    pv: "$(P)userCalcEnable.VAL"
    
    geometry: 24x24
    square: true
```


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


* **Example**

```yaml
- !Menu
    foreground: *black
    background: *edit_blue
    geometry: 355x0 x 80x20
    pv: $(P){Instance}:EnableCallbacks
```


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


* **Example**

```yaml
- !TextEntry
    geometry: 5x0 x 120x20
    
    pv: "$(P)$(R)Description"
    
    alignment: { vertical: bottom }
```


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


* **Example**

```yaml
- !TextMonitor
    geometry: 5x0 x 120x20
    
    pv: "$(P)$(R)Description_RBV"
    
    alignment: { horizontal: right }
```
