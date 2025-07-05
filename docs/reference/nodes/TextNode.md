---
layout: default
title: TextNode
parent: Nodes
nav_order: 35
has_toc: false
---


# TextNode

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