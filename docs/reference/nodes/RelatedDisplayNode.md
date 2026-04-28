---
layout: default
title: RelatedDisplayNode
parent: Nodes
nav_order: 24
has_toc: false
---


# RelatedDisplayNode

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
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Examples**

```yaml
- !RelatedDisplay
    geometry: 120x30
    background: *menu_green
    foreground: *white
    text: "Motor Details"

    links:
        - { label: "Help",  file: "motorx_help",  macros: "P=$(P),M=$(M)" }
        - { label: "More",  file: "motorx_more",  macros: "P=$(P),M=$(M)" }
        - { label: "Setup", file: "motorx_setup", macros: "P=$(P),M=$(M)" }
        - { label: "All",   file: "motorx_all",   macros: "P=$(P),M=$(M)" }
```

The file extension is automatically appended based on the output format.
The `replace` option can be used to open the display in the same window:

```yaml
- !RelatedDisplay
    geometry: 100x20
    text: "Open"
    links:
        - { label: "Main", file: "main_screen", macros: "P=$(P)", replace: true }
```