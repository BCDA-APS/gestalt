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
"ByteMonitor", "CheckBox", "ChoiceButton", "ComboBox", "DataBrowser", "Ellipse", "EmbeddedDisplay", 
"FileSelector", "Group", "Image", "LED", "LEDMultiState", "Label", "Meter", "NavigationTabs", 
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


### Form

---

A special widget used to set values for the top-level window.


* **Special Attributes**

|    Name   |  Type  | Description|
|-----------|--------|------------|
| geometry  | Rect   | A rectangle describing the position and dimensions of the widget |
| margins   | Rect   | A set of numbers describing the number of pixels to leave clear on the left, top, right, and bottom of the window respectively |


* **Example**  

```yaml
Form: !Form
    styleSheet: !string "QWidget#Form {background: rgba(187, 187, 187, 255);}\nQPushButton::menu-indicator {image: url(none.png); width: 0}"

    margins: 5x5x5x5
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

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |


* **Example**

```yaml
- !Text
    geometry: 5x0 x 120x20
    
    text: "Label Text"
    font: -Liberation Sans - bold - 12
```
