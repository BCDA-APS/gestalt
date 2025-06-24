{% include header.md title='EllipseNode' parent='Nodes' nav_order=9 %}
<a id="EllipseNode"></a>

# EllipseNode

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

