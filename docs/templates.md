---
layout: default
title: Creating a Template
nav_order: 4
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
have been tagged with a supported widget type from the list in [widgets](reference/nodes/Widgets.md). 
Properties of the Widget can then be set within the element.

```yaml 
small_rect_widget: !Rectangle
    geometry: 100x100
    background: $000000
```

Capitalization is loose and can be specified with all-caps, all-lowercase, capitalization 
matching the name in the list of widgets, or with just the first letter capitalized (if 
that's different from the normal name).


## Data Types

As seen above, Gestalt can automatically infer the data type of certain structures.
For example, in the previous snippets, the geometry property is set to '100x100'. 
This is recognized as a two element Rect structure defining the width and height of 
a widget. Any bare scalar element (no quotes, no special characters) that consists 
of two numbers separated by an 'x' will be interpreted in this way. 

Occasionally, parsing might be ambiguous between different data types. In that instance,
you may need to provide an explicit specifier. A primary example of this is if you are
specifically defining a Qt widget and are trying to set an enumeration value that does 
not use the double-colon standard.

```yaml
more_screens: !caRelatedDisplay
    stackingMode: !enum Menu   
```

However, the output-independent widgets that are recommended all set the types of their
parameters automatically, so no specification is needed.

The full list of explicit data type tags that are currently recognized and their 
implicit parsing are listed here:


* **'!bool'** - A python boolean value, see yaml specification for implicit resolution

* **'!double'** - A double value, see yaml specification for implicit resolution

* **'!number'** - An integer value, see yaml specification for implicit resolution

* **'!string'** - A string of characters, see yaml specification for implicit resolution

* **'!color'** - A color value, will recognize a set of hexadecimal digits after a '$'
character. Either '$RRGGBB' or '$RRGGBBAA'

* **'!font'** - A Font specification, will recognize a dash followed by a font name.
Optionally, extra dashes can also specify font style and size. '-DejaVu Sans Mono - regular - 16'

* **'!geom'** - A rectangle geometry, will recognize numbers separated by an 'x' character.
Either 'Width x Height' or 'X x Y x Width x Height'

* **'!align'** - A font alignment, will recognize a combined set of words in the form of
VerticalHorizontal. Vertical can be any of "Top, Bottom, Center, or Middle". Horizontal can
be any of "Left, Right, Center, or Middle". If both Horizontal and Vertical are to be centered
you can use just a single instance of Center or Middle.

* **'!enum'** - A menu selection, will recognize a value that contains a double-colon within.
(Necessary for Qt only)  

* **'!set'** - A grouped enumeration, will recognize multiple enums separated by the '|'
character. (Necessary for Qt only)  


## Included Files

Unlike standard yaml files, layout files have the capability to include other yml
files to provide reuseability. There are a set of useful yml files already included 
with Gestalt in the /widgets folder.

colors.yml provides a set of named colors that can be used instead of constantly specifying
hex values. The naming convention matches up with the full list of CSS colors, alongside
some specially named ones like 'alarm_red' and 'edit_blue' that match up with frequently
used conventions in MEDM. These colors are specified as aliases, so can be used in
widget properties using the '*' dereference character.

```yaml
#include colors.yml

UITitle: !hstretch:Text
    geometry: 0x45
    foreground: *white
    background: *header_blue
    border-color: *black
    border-width: 3
            
    text: "{TITLE}"
    font: -Cantarell - Bold - 16
    alignment: Center
```

color-schemes.yml contains a set of default values that get used often. These can be applied to widgets
of the correct type with the "<<" insert operator.

```yaml
#include color-schemes.yml

a_LED: !LED
    <<: *alarm_led
    pv: "$(P)Bi{N}.VAL"                   
    geometry: 15x0 x 22x22
```

And then there are a handful of useful groups of widgets that can be used to quickly build
common styles of screens. widgets.yml is a file that will include all of the existing
sets of these groups, or you can include files individually. Information about the files
and the groups of widgets that are contained can be found in the [Reference](reference/templates/index.md).

```yaml
#include widgets.yml

indicator_light: !Apply:OnOffLED
    control-pv: "$(P)$(M).CNEN
```
