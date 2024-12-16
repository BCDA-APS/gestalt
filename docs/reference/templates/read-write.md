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
Enabled elements are displayed in a horizontal row in the order shown above.

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


* **Example**

```yaml
SelectFunction: !Apply:PVReadWrite
    label: "Function:"
    menu-pv: "$(P)$(R)1:FUNC"
    read-pv: "$(P)$(R)1:FUNC:RBV"
```
