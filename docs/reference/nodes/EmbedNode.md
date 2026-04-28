---
layout: default
title: EmbedNode
parent: Nodes
nav_order: 10
has_toc: false
---


# EmbedNode

A special tag used to allow templates to be able to recieve portions of their contents when being applied.

The embed tag notes the name of a macro that should contain a section of UI layout. This layout will then be
included directly alongside the rest of the template when applied. Allowing for uses like wrapping arbitrary
sets of elements in the same style frame.

* **Examples**

```yaml
_TitledSection: !Template:TitledSection
    - !Defaults
        title: ""
        content:
            - !Spacer

    - !Group
        border-width: 1
        border-color: *black
        margins: 5x0x5x10
        geometry: 350x0
        
        children:
            Title: !HCenter:Text
                geometry: 0x1 x 110x22
                background: $DADADA
                foreground: *header_blue
                alignment: Center
                text: "{title}"
        
            Flow: !HCenter:VFlow 
                geometry: 0x34 x 0x0
                padding: 10
                children: 
                    - !Embed:content
```

The caller provides content to fill the embed slot:

```yaml
Status: !Apply:TitledSection
    title: "Device Status"
    content:
        - !VFlow
            padding: 5
            children:
                - !TextMonitor { geometry: 120x20, pv: "$(P)$(R)Status_RBV" }
                - !TextMonitor { geometry: 120x20, pv: "$(P)$(R)Value_RBV" }
```