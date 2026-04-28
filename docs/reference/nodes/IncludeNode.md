---
layout: default
title: IncludeNode
parent: Nodes
nav_order: 15
has_toc: false
---


# IncludeNode

A widget that references and embeds another UI file


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| file       | String | The filepath of the file to display |
| macros     | String | An msi formatted macro string to provide the display file |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
EmbeddedDisplay: !Include
    geometry: 490x125
    file: "motorx_all"
    macros: "P=$(P),M=$(M)"
```

The file extension is automatically appended based on the output format
(.ui for Qt, .bob for Phoebus).