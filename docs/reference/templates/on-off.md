---
layout: default
title: on-off.yml
parent: Templates
nav_order: 2
---

# on-off.yml
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### OnOffText

Two overlaid colored labels, where only one of the two labels will display at any one time,
with visibility controlled by a user-specified pv. When the pv is 0, the off label will be
displayed. Otherwise, the on label will show.


* **Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| height       | Number | The height of the resulting Text nodes, default: 20 |
| width        | Number | The width  of the resulting Text nodes, can be referenced as text-width for backwards compatibility, default: 20 |
| geometry     | Rect   | Can specify geometry instead of setting width and height separately, default: "{width}x{height}" |
| control-pv   | String | The full pv for the pv that controls visibility, can be referenced as PV for backwards compatibility |
| on-label     | String | Text to display when control-pv is non-zero, default: "On" |
| off-label    | String | Text to display when control-pv is zero, default: "Off" |
| on-color     | Color  | Color of on-label, default: *alarm_green |
| off-color    | Color  | Color of off-label, default: *alarm_red  |
| fontname     | String | Name of font for display text, default: "Liberation Sans" |

* **Example**

```yaml
PowerControlReadback: !Apply:OnOffText
    width: 100
    height: 50
    control-pv: "$(P)$(R)1:OUT:RBV"
    
    on-color: *menu_green
```


### OnOffLED

A circular colored button that toggles state when pressed. 

* **Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| size         | Number | Controls both height and width at the same time, useful because most times LED will be a circle. default: 16 |
| height       | Number | The height of the resulting LED node, default: "{size}" |
| width        | Number | The width  of the resulting LED node, default: "{size}" |
| geometry     | Rect   | Can specify geometry instead of setting width and height separately, default: "{width}x{height}" |
| control-pv   | String | The full pv for the pv that controls visibility |
| on-label     | String | Text to display on top of LED when control-pv is non-zero, can be referenced as on-text for backwards compatibility, default: "1" |
| off-label    | String | Text to display on top of LED when control-pv is zero, can be referenced as off-text for backwards compatibility, default: "0" |
| on-color     | Color  | Color of LED when control-pv is non-zero, default: *alarm_green |
| off-color    | Color  | Color of LED when control-pv is zero, default: *alarm_red  |
| fontname     | String | Name of font for display text, default: "Liberation Sans" |

* **Example**

```yaml
TorqueToggle: !Apply:OnOffLED
    size: 16
    control-pv: "$(P)$(M).CNEN"
```
