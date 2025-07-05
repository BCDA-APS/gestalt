---
layout: default
title: ApplyNode
parent: Nodes
nav_order: 2
has_toc: false
---


# ApplyNode

Apply and Template are special tags that are used to save and restore sets of nodes and provide
them with user-defined macros to fill out their attributes. Both apply and template are tags applied
to a name that gets associated with the set of nodes. 

So, when defining a template that you wish to refer to as "io_label", you would use the type 
"!Template:io_label". Then, when including those templated nodes into a different part of your
yaml file, you would use "!Apply:io_label".

A Template definition is a list with a single Node and an optional set of defaults for the macros used
within the Template. Defaults are just a dictionary of names and values, but can be tagged with the do-nothing 
tag "!Defaults" to make the intention clear. 

For the Apply node, its definition is a dictionary with a set of macros you wish to provide the Template.

* **Example**

```yaml

LblRbkTemplate: !Template:lbl_rbk
    - !Defaults
        spacing: 10
        
    - !hflow
        padding: "{spacing}"
        
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