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


### Apply/Template

---

Apply and Template are special tags that are used to save and restore sets of nodes and provide
them with user-defined macros to fill out their attributes. Both apply and template are tags applied
to a name that gets associated with the set of nodes. 

So, when defining a template that you wish to refer to as "io_label", you would use the type 
"!Template:io_label". Then, when including those templated nodes into a different part of your
yaml file, you would use "!Apply:io_label".

A Template definition is a list with (currently) only a single Node within. While an Apply
definition is a dictionary with a set of macros you wish to provide the Template.

* **Example**

```yaml

LblRbkTemplate: !Template:lbl_rbk
    - !hflow
        padding: 10
        
        children:
            - !Text { geometry: 150x20, text: "{TITLE}" }
            - !TextMonitor
                <<: *FixedFeedback
                pv: "$(P){PV}"


Status: !hcenter:hflow
    geometry: 20x65 x 0x0
    padding: 20

    children:
        - !vflow
            padding: 5
        
            children:
                - !Apply:lbl_rbk { TITLE: "Model Name",  PV: "ModelName" }
                - !Apply:lbl_rbk { TITLE: "Serial Num",  PV: "SerialNumber" }                            
                - !Apply:lbl_rbk { TITLE: "LJM Version", PV: "LJMVersion" }
                    
        - !vflow
            padding: 5
        
            children:
                - !Apply:lbl_rbk { TITLE: "Firmware Version", PV: "FirmwareVersion" }                    
                - !Apply:lbl_rbk { TITLE: "Temperature (C)",  PV: "DeviceTemperature" }
                - !Apply:lbl_rbk { TITLE: "Driver Version",   PV: "DriverVersion" }

```


### Conditional

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

