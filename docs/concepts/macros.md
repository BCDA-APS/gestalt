---
layout: default
title: Macro Resolution
parent: Concepts
nav_order: 2
---

# Macro Resolution
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

When a property value contains `{name}`, resolution is deferred until generation time.
At that point, the macro is looked up in the current macro environment and substituted.
See [Core Concepts](./#templates-and-apply) for the basics of how macros and templates
work.


## Macro environment

The macro environment is built from three sources, in order of precedence:

1. **Apply overrides** -- Values provided at the `!Apply` call site.
2. **Template defaults** -- Default values from the `!Defaults` block.
3. **Data file values** -- External input data provided via `--input`.


## Recursive resolution

Resolution is recursive -- a macro can resolve to a value that itself contains further
macros, which are then resolved in their own turn:

```yaml
- !Defaults
    height: 20
    label-height: "{height}"
    label-geometry: "100x{label-height}"
```

Setting `height: 30` at apply time causes `label-height` to resolve to `"30"`, which
in turn causes `label-geometry` to resolve to `"100x30"`.

Macros that cannot be resolved (because no matching key exists in the environment) are
left in place as literal `{name}` text. This partial substitution allows macros to pass
through multiple layers of template nesting before reaching their final value.


## Python format string syntax

Under the hood, macro substitution uses Python's `str.format_map()`. This means the
full [Python format string syntax](https://docs.python.org/3/library/string.html#formatstrings)
is available in property values.

**Format specifications** -- control number formatting, padding, etc.:

```yaml
pv: "$(P)Ch{N:02d}:Value"        # N=3  --> "$(P)Ch03:Value"
text: "Gain: {gain:.2f}"         # gain=1.5 --> "Gain: 1.50"
```

**Dictionary access** -- index into dict-valued macros:

```yaml
text: "{channel[label]}"         # channel={label: "Temp", pv: "T1"} --> "Temp"
pv:   "{channel[pv]}:RBV"       # --> "T1:RBV"
```


## EPICS macros

EPICS macros like `$(P)` use a different syntax (`$()` vs `{}`) and are left untouched
by Gestalt. They are resolved later by the display manager at runtime.

---

## Next steps

- [Architecture](architecture) -- How Gestalt processes layout files.
- [Core Concepts](./) -- Nodes, data types, includes, templates, and output formats.
