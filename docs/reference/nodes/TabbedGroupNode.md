---
layout: default
title: TabbedGroupNode
parent: Nodes
nav_order: 30
has_toc: false
---


<a id="TabbedGroupNode"></a>

# TabbedGroupNode

A widget representing a stack of display areas, with each only being displayed upon the user clicking a corresponding tab button.

The 'children' attribute works slightly differently for this layout. Each individual child node must be a '!Tab'. Tabs are pass-through
Group nodes, with the children attribute specifying the widgets that are displayed for that tag.

Each child node in the TabbedGroup will be associated with a specific tab, and selecting that tab will display all the
widgets that are in the corresponding '!Tab'. If one defines the 'children' attribute as a dictionary, then the key values will
be used as the tab names. If 'children' is a list, then the tabs will display as "Tab 1", "Tab 2", etc.

The macros __parentwidth__ and __parentheight__ will be passed along to children widgets, these are set to the size of the display
pane, which will depend on the values of certain attributes.


* **Special Attributes**

|     Name     |    Type   | Description|
|--------------|-----------|------------|
| geometry     | Rect      | A rectangle describing the position and dimensions of the widget |
| children     | List/Dict | A set of '!Tab's describing the individual display panes that are contained by this group |
| foreground   | Color     | The color of the text for each tab, defaults to $000000 |
| background   | Color     | The fill color for each display pane, defaults to $00000000 |
| tab-color    | Color     | The background color for each tab, defaults to $D2D2D2 |
| selected     | Color     | The background color for the currently selected tab, defaults to $A8A8A8 |
| border-color | Color     | The color of the border that surrounds the display panes, defaults to $000000 |
| border-width | Number    | The thickness of the group's border in pixels, defaults to 0 |
| padding      | Number    | The number of pixels between each tab, defaults to 5 |
| inset        | Number    | The number of pixels to horizontally offset the tab bar from the display pane, defaults to 0 |
| offset       | Number    | The number of pixels to vertically offset the display pane from the tab bar, defaults to 0 |
| tabbar-height| Number    | The number of pixels out of the total widget height to devote to the tab bar (includes the above offset), defaults to 10% of height |
| font         | Font      | The display font for the tabs, defaults to Liberation Sans 12 |


* **Example**

```yaml
- !TabbedGroup
    geometry: 570x200

    inset: 5
    offset: 3

    border-color: *header_blue
    tab-color: *header_blue
    foreground: *white
    selected: $3970C4

    font: -DejaVu Sans Mono - Bold - 9

    children:
        Motors: !Tab
            children:
                - !AStretch:Spacer

        Optics: !Tab
            children:
                - !AStretch:Spacer

        Detectors: !Tab
            children:
                - !AStretch:Spacer

        Direct I/O: !Tab
            children:
                - !AStretch:Spacer

        Devices: !Tab
            children:
                - !AStretch:Spacer

        Tools: !Tab
            children:
                - !AStretch:Spacer
```

To save space, the !Tab node type can be directly applied to the list of children nodes.

```yaml
- !TabbedGroup
    geometry: 570x200

    inset: 5
    offset: 3

    border-color: *header_blue
    tab-color: *header_blue
    foreground: *white
    selected: $3970C4

    font: -DejaVu Sans Mono - Bold - 9

    children:
        Motors: !Tab
            - !AStretch:Spacer

        Optics: !Tab
            - !AStretch:Spacer

        Detectors: !Tab
            - !AStretch:Spacer

        Direct I/O: !Tab
            - !AStretch:Spacer

        Devices: !Tab
            - !AStretch:Spacer

        Tools: !Tab
            - !AStretch:Spacer
```

