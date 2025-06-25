---
layout: default
title: IncludeNode
parent: Nodes
nav_order: 15
has_toc: false
---


<a id="IncludeNode"></a>

# IncludeNode

A widget that references and embeds another UI file


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| file       | String | The filepath of the file to display |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
EmbededDisplay: !Include
    file: "another_file"  # Can leave off file extension, will be appended with correct filetype for the output UI tool
```

