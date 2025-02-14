---
layout: default
title: link-grid.yml
parent: Templates
grand_parent: Reference
nav_order: 5
---

# link-grid.yml
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### RelatedDisplayGrid

Arranges a list of Related Display widgets in a grid

Information for each Related Display widget should be a dictionary that has two keys, title and links. 
Title being a string providing the text for the button, with links being a list of dictionaries set up
the same way as the links attribute of the Related Display widget.


* **Attributes**

|     Name          |  Type  | Description|
|-------------------|--------|------------|
| buttons           | List   | A List or reference to a list of dictionaries providing information about the Related Display | 
| button-width      | Number | The width of each Related Display  |
| button-height     | Number | The height of each Related Display |
| button-background | Color  | The background color of each Related Display |
| button-foreground | Color  | The foreground color of each Related Display |
| aspect-ratio      | Number | The suggested ratio of elements wide to elements tall |
| padding           | Number | Number of pixels between each Related Display |
| margins           | Rect   | Outside margins around entire Grid |


* **Example**

```yaml
Motors:
    - title: "Motors 1-8"
      links:
        - {label: "Motors 1-8",   file: "topMotors8", macros: "P=ioc:,M1=m1,M2=m2,M3=m3,M4=m4,M5=m5,M6=m6,M7=m7,M8=m8"}

Optics:
    - title: ""
      links: 
        - {label: "", file: "", macros: ""}

Links: !TabbedGroup
    foreground: *white
    tab-color: $003584
    selected: $3970C4
    border-color: $003584
    border-width: 3
    inset: 10
    offset: 5
    padding: 10
    font: -DejaVu Sans Mono -Bold -9

    geometry: 0x75 x 860x240

    children:
        Motors: !Tab
            - !Apply:RelatedDisplayGrid { buttons: "Motors" }
        Optics: !Tab
            - !Apply:RelatedDisplayGrid { buttons: "Optics" }

```
