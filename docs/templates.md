---
layout: default
title: Templates
nav_order: 2
---

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


## Template Files

Templates are YAML files that describe the structure of the UI file to be generated.
These files are parsed by Gestalt into a graph of nodes which can represent individual
widgets to generate, structures of widgets, various means of laying out widgets, or
logical statements that can affect the outcome of the previous types. Structured input 
data can be combined with the graph to then generate the output screen.


## Widgets

The basic element of a template file is a Widget node. These are YAML elements that
have been tagged with a supported widget type from Qt or CSS-Phoebus. Properties of
the Widget can then be set within the element.

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

All caQtDM-specific and most CSS-Phoebus widgets are supported, only the Image,
Strip Chart, and X/Y Plot aren't supported due to the restrictions of the phoebusgen
library. Widget class names are just the name of the Widget in their respective 
program. Capitalization is loose and can be specified with all-caps, all-lowercase,
capitalization matching the program, or with the first letter capitalized (if that's
different from the normal name).


## Data Types

As seen above, Gestalt can automatically infer the data type of certain structures.
For example, in the previous snippets, the geometry property is set to '100x100'. 
This is recognized as a two element Rect structure defining the width and height of 
a widget. Any bare scalar element (no quotes, no special characters) that consists 
of two numbers separated by an 'x' will be interpreted in this way. 

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


## Included Files

Unlike standard yaml files, layout files have the capability to include other yml
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
