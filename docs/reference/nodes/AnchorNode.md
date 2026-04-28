---
layout: default
title: AnchorNode
parent: Nodes
nav_order: 1
has_toc: false
---


# AnchorNode

A positioner used to place a widget along the edge of its parents area

### HAnchor

---

Positions a widget at the horizontal extent of its parent node.


* **Example**

```yaml
WideGroup: !Group
    geometry: 400x30
    children:
        - !HAnchor:RelatedDisplay
            geometry: 120x30
            background: *menu_green
            foreground: *white
            text: "More"
            links:
                - { label: "Details", file: "details", macros: "P=$(P)" }
```



### VAnchor

---

Positions a widget at the vertical extent of its parent node.

You may also use the alias "anchor" to reference the vanchor node.


* **Example**

```yaml
TallGroup: !Group
    geometry: 200x400
    children:
        - !VAnchor:Text
            geometry: 200x20
            text: "Bottom Label"
            alignment: Center
```


### AAnchor

---

Positions a widget to be in the lower right corner of its parent node.


* **Example**

```yaml
BigGroup: !Group
    geometry: 400x400
    children:
        - !AAnchor:Text
            geometry: 80x20
            text: "Corner"
```