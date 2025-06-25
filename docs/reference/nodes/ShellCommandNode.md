---
layout: default
title: ShellCommandNode
parent: Nodes
nav_order: 27
has_toc: false
---


<a id="ShellCommandNode"></a>

# ShellCommandNode

A button that will trigger the running of a selected shell command

These shell commands are detailed by the attribute `commands` which is a list of
dictionaries. Within each dictionary, the following values can be defined:

* label   - The display name for the command to run
* command - The command and all arguments that will be executed

<br>


* **Special Attributes**

|    Name    |  Type  | Description|
|------------|--------|------------|
| geometry   | Rect   | A rectangle describing the position and dimensions of the widget |
| text       | String | The widget's display text |
| foreground | Color  | Widget foreground color |
| background | Color  | Widget background color |
| font       | Font   | Widget display font |
| commands   | List   | A list of dictionaries describing the commands that can be run |
| visibility | String | A pv that determines the visibility of the widget, visibility is turned off if the PV's value is zero. This logic is inverted if the !Not tag is used instead of String |


* **Example**

```yaml
ExampleCommand: !ShellCommand
    geometry: 10x10 x 80x20

    text: "Say"

    commands: 
        - { label: "Hello",   command: "echo 'Hello'"  }
        - { label: "Goodbye", command: "echo 'Goodbye'"}
```

