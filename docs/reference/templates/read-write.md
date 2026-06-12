---
layout: default
title: read-write.yml
parent: Templates
grand_parent: Reference
nav_order: 3
---

# read-write.yml
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}


### PVReadWrite

A horizontal flow of optional elements for ease of implementation of simple writing to a pv with a readback display.
The possible elements that are included are:

* a Text label for providing the user with notification of what they are editing  
* a TextEntry description field, for editing the DESC field or similar pv  
* a TextEntry input field, if the pv would use user-defined text/number values  
* a Menu input field, for if the pv is a selectable enum  
* a MessageButton input field, for if the pv is just something that needs to be PROC'd or similar
* a TextMonitor readback field, for displaying a readback pv value
* a Text label for appending units onto the readback

Each of the elements are disabled by default and enabled by providing a value for their text (for labels) or pv (for input/output fields).
By default, enabled elements are displayed in a horizontal row in the order shown above. The attribute "read-first" will move the readback
and units label before the input fields, but still after the description.

* **Attributes**

|     Name        |  Type  | Description|
|-----------------|--------|------------|
| height          | Number | The height of all resulting nodes, default: 20 |
| element-width   | Number | Can specify the default width for all resulting nodes, default: 60 |
| label-width     | Number | Width for the label element, default: "{element-width}" |
| desc-width      | Number | Width for the description element, default: "{element-width}" |
| entry-width     | Number | Width for the basic text entry element, default: "{element-width}" |
| menu-width      | Number | Width for the menu input element, default: "{element-width}" |
| button-width    | Number | Width for the MessageButton element, default: "{element-width}" |
| read-width      | Number | Width for the readback element, default: "{element-width}" |
| units-width     | Number | Width for the units element, default: "{element-width}" |
| spacing         | Number | Spacing between any two enabled elements, default: 15   |
| /////////////// | ////// | /////////////////////////////////////////////////////// |
| editable-color  | Color  | Default color for the general input fields (entry, menu, button), default: *edit_blue |
| label-background| Color  | Background color for the label element, default: *transparent |
| desc-background | Color  | Background color for the description element, default: *grey_light |
| entry-background| Color  | Background color for the basic text entry element, default: "{editable-color}" |
| menu-background | Color  | Background color for the menu input element, default: "{editable-color}" |
| button-background|Color  | Background color for the MessageButton element, default: "{editable-color}" |
| read-background | Color  | Background color for the readback element, default: *transparent |
| units-background| Color  | Background color for the units element, default: *transparent |
| /////////////// | ////// | /////////////////////////////////////////////////////// |
| text-color      | Color  | Default color for the text used in all elements, default: *black |
| label-foreground| Color  | Text color for the label element, default: "{text-color}" |
| desc-foreground | Color  | Text color for the description element, default: "{text-color}" |
| entry-foreground| Color  | Text color for the basic text entry element, default: "{text-color}" |
| menu-foreground | Color  | Text color for the menu input element, default: "{text-color}" |
| button-foreground|Color  | Text color for the MessageButton element, default: "{text-color}" |
| read-foreground | Color  | Text color for the readback element, default: "{text-color}" |
| units-foreground| Color  | Text color for the units element, default: "{text-color}" |
| /////////////// | ////// | /////////////////////////////////////////////////////// |
| label           | String | Display text for label element |
| desc-pv         | String | Connected pv for description element | 
| entry-pv        | String | Connected pv for basic text entry element | 
| menu-pv         | String | Connected pv for menu input element | 
| button-pv       | String | Connected pv for MessageButton element | 
| read-pv         | String | Connected pv for readback element |
| units           | String | Display text for units element | 
| button-text     | String | Display text for MessageButton element | 
| button-value    | String | Value to send MessageButton pv |
| /////////////// | ////// | /////////////////////////////////////////////////////// |
| read-first      | Bool   | Swaps the location of the output fields and the readback |


* **Example**

```yaml
SelectFunction: !Apply:PVReadWrite
    label: "Function:"
    menu-pv: "$(P)$(R)1:FUNC"
    read-pv: "$(P)$(R)1:FUNC:RBV"
```

---

### ReadbackList

A vertical list of labeled readback rows. Takes a list of `{label, pv}` dictionaries and renders
each as a horizontal pair of a text label and a TextMonitor readback widget. Useful for status
panels, device info displays, and any read-only summary of PV values.

Each row dictionary must have `label` and `pv` keys. Rows can optionally include `format` and
`precision` keys to override the template-level defaults for individual rows.

* **Attributes**

|     Name          |  Type     | Description|
|-------------------|-----------|------------|
| rows              | List      | A list of dictionaries, each with `label` and `pv` keys. Optional `format` key per row |
| label-width       | Number    | Width of the label column, default: 100 |
| read-width        | Number    | Width of the readback column, default: 120 |
| height            | Number    | Height of each row, default: 20 |
| padding           | Number    | Vertical spacing between rows, default: 5 |
| spacing           | Number    | Horizontal spacing between label and readback, default: 5 |
| read-foreground   | Color     | Text color for readback values, default: *header_blue |
| read-background   | Color     | Background color for readback values, default: *transparent |
| label-foreground  | Color     | Text color for labels, default: *black |
| label-background  | Color     | Background color for labels, default: *transparent |
| label-alignment   | Alignment | Text alignment for labels, default: CenterRight |
| read-alignment    | Alignment | Text alignment for readback values, default: CenterRight |
| fontname          | String    | Font family for all text, default: "Liberation Sans" |
| format            | String    | Default display format for readback values, default: "String" |


* **Examples**

```yaml
DeviceInfo: !Apply:ReadbackList
    label-width: 120
    read-width: 150
    rows:
        - { label: "Model",    pv: "$(P)$(R)Model_RBV" }
        - { label: "Serial",   pv: "$(P)$(R)SerialNumber_RBV" }
        - { label: "Firmware", pv: "$(P)$(R)FirmwareVersion_RBV" }
        - { label: "Temp (C)", pv: "$(P)$(R)Temperature_RBV" }
```

With per-row format overrides:

```yaml
MixedReadbacks: !Apply:ReadbackList
    label-width: 100
    read-width: 100
    rows:
        - { label: "Name",  pv: "$(P)$(R)Name_RBV" }
        - { label: "Value", pv: "$(P)$(R)Value_RBV", format: "Decimal" }
        - { label: "Temp",  pv: "$(P)$(R)Temp_RBV",  format: "Engineering" }
```
