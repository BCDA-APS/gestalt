---
layout: default
title: Logical Groups
parent: Nodes
nav_order: 2
---

# Layouts
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

### conditional

---

Conditionally adds children widgets into the final output based upon a specified macro in the
input data.

The macro named by the `condition` macro is parsed and treated as a truthy value in python. If
the macro's data is equivalent to a true value, then the conditional's contents are included in
the resulting UI screen. Otherwise, none of the children widgets are included.

* **Special Attributes**

|     Name     |  Type  | Description|
|--------------|--------|------------|
| children     | List   | A list of widgets to conditionally include |
| condition    | String | The name of a macro that will determine the children widget's inclusion |
| background   | Color  | A fill color behind the entirety of all children |
| border-color | Color  | The color of the group's border surrounding the children widgets |
| border-width | Number | The thickness of the group's border in pixels |

* **Example**

```yaml
- !conditional
    condition: "INCLUDE_LED"
    
    geometry: 0x20 x 0x0
    
    children:
        - !caLed
            channel: !string "xxx:yyy:bi.VAL"
            trueColor: *alarm_red
            falseColor: *alarm_green
            
            borderColor: *transparent
            
            gradientEnabled: false
            
            geometry: 15x0 x 22x22
```

