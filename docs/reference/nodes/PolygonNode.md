---
layout: default
title: PolygonNode
parent: Nodes
nav_order: 21
has_toc: false
---


# PolygonNode

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