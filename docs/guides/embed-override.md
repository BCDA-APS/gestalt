---
layout: default
title: Overridable Defaults
parent: Guides
nav_order: 6
---

# Overridable Defaults
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

The `!Embed` node lets template authors accept arbitrary widget content from callers
and expand it in-place within the template's layout.


## How Embed works

`!Embed:parameter-name` references a parameter in the current macro environment whose
value is a list of nodes. At generation time, the embed expands those nodes in-place,
as if they were written directly at the embed's location in the layout.

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
                geometry: "0x1 x 110x22"
                background: $DADADA
                foreground: *header_blue
                alignment: Center
                text: "{title}"

            Flow: !HCenter:VFlow
                geometry: "0x34 x 0x0"
                padding: 10
                children:
                    - !Embed:content
```

Here, `!Embed:content` looks up the `content` parameter -- which is a list of nodes --
and expands each item as a child of the VFlow. The default is a single `!Spacer`, but
the caller provides the real content:

```yaml
Status: !Apply:TitledSection
    title: "Device Status"
    content:
        - !TextMonitor { geometry: 120x20, pv: "$(P)$(R)Status_RBV" }
        - !TextMonitor { geometry: 120x20, pv: "$(P)$(R)Value_RBV" }
```

The two TextMonitor nodes are expanded in-place inside the VFlow, as if they had been
written there directly. The `TitledSection` template provides the surrounding frame
and title -- the caller provides whatever widgets belong inside it.

The parameter value must be a list. Each item in the list is applied individually,
so a list of three widgets produces three children at the embed location.


## Embed for overridable defaults

The same mechanism enables overridable widget defaults in templates. The idea is to
define a default widget list in one parameter and reference it through an embed in
another:

```yaml
_FlexRow: !Template:FlexRow
    - !Defaults
        read-width: 80

        read-default:
            - !TextMonitor
                geometry: "0x0x{read-width}x20"
                pv: "{read-pv}"
                background: *transparent

        read-element: [ !Embed:read-default ]

    - !HFlow
        padding: 5
        children:
            - !Text { geometry: "100x20", text: "{label}" }
            - !VCenter:Embed:read-element
```

The indirection works like this:

1. `read-default` holds the default widget as a list of nodes.
2. `read-element` is set to `[ !Embed:read-default ]` -- a list containing a single
   embed that references `read-default`. When expanded, this produces the same nodes
   as `read-default`.
3. The HFlow uses `!Embed:read-element` to place the content.

With no overrides, the caller gets the default TextMonitor. But they can replace the
entire widget by overriding `read-element` with a different node list:

```yaml
# Use the default readback
Normal: !Apply:FlexRow
    label: "Temperature"
    read-pv: "$(P)Temp:RBV"

# Override with a custom readback
Custom: !Apply:FlexRow
    label: "Temperature"
    read-pv: "$(P)Temp:RBV"
    read-element:
        - !TextMonitor
            geometry: "0x0x120x20"
            pv: "$(P)Temp:RBV"
            foreground: *alarm_red
            alarm-border: true
```

This gives callers two levels of customization:

1. **Tweak properties**: Override `read-width` or other parameters that feed into the
   default widget definition.
2. **Replace entirely**: Override `read-element` with a completely different node list.


## Nested template defaults

The default widget definition can itself use `!Apply` to instantiate another template.
The macro environment flows through -- inner templates can see outer scope macros
without explicit pass-through:

```yaml
_ToggleRow: !Template:ToggleRow
    - !Defaults
        enable-default:
            - !Apply:OnOffLED
                geometry: "0x0x{enable-width}x{enable-height}"
                control-pv: "{enable-pv}"
                square: "{enable-square}"

        enable-element: [ !Embed:enable-default ]

    - !HFlow
        children:
            - !VCenter:Embed:enable-element
            - !Text { geometry: "100x20", text: "{label}" }
```

The `{enable-pv}`, `{enable-width}`, `{enable-height}`, and `{enable-square}` macros
are resolved from the caller's parameter set and passed through to the inner
`!Apply:OnOffLED` automatically.


## Design guidelines

1. **Use the two-part pattern** (`*-default` and `*-element`) for each overridable
   widget. This is the established convention in the built-in templates.

2. **Keep defaults self-contained**. Each `*-default` block should be a complete widget
   definition that works with just the template's own parameters.

3. **Document which parameters are passed through** to nested templates, especially when
   using macro flow-through instead of explicit parameter passing.

---

## Next steps

- [Conditional Elements](conditionals) -- Optionally show or hide elements with `!If`.
- [Custom Templates](custom-templates) -- Fundamentals of writing templates.
- [PVReadWrite Reference](../reference/templates/read-write) -- See these patterns in the full built-in template.
