---
layout: default
title: Architecture
parent: Concepts
nav_order: 1
---

# Architecture
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

This page describes how Gestalt works at a high level -- from reading a YAML layout
file to writing a platform-specific screen file.


## Processing pipeline

Gestalt processes a layout in three stages:

```
Layout YAML  -->  Node Tree  -->  Output File
   (parse)        (generate)       (write)
```

1. **Parse**: The YAML layout file is read and converted into a tree of Node objects.
   Includes are resolved, templates are registered, and YAML tags are mapped to node
   classes.

2. **Generate**: A platform-specific generator walks the node tree. Each node produces
   one or more widgets in the generator's internal representation. Layout nodes compute
   positions, repeat nodes duplicate their children, and template applies resolve macros.

3. **Write**: The generator's output representation is serialized to a file -- XML for
   caQtDM `.ui` files, Phoebus XML for `.bob` files, or Qt-compatible XML for PyDM `.ui`
   files.


## Parsing

The `Stylesheet` module handles the parse stage. It uses a custom YAML loader with
registered constructors for each YAML tag.

When the parser encounters a tag like `!TextMonitor`, it calls the corresponding
constructor, which creates a Node object with the tag's properties stored as a
dictionary of typed values.

### Include resolution

`#include` directives are processed as a pre-parse step. The file is read line by line,
and each `#include filename` line is replaced with the contents of the referenced file.
The search path is:

1. The directory of the file containing the `#include`.
2. Gestalt's built-in `widgets/` directory.
3. Any directories specified with `--include`.

### Template registration

When the parser encounters a `!Template:Name` tag, it registers the template definition
in a global template dictionary. Later `!Apply:Name` tags look up the template by name
and create a copy of its node tree with the provided macro overrides.


## Node tree

After parsing, the layout is represented as an ordered list of named top-level nodes.
Each node may contain child nodes (e.g., a FlowNode contains widget children), forming
a tree. Each node stores its properties as typed values that support automatic data
type inference and deferred macro substitution.

See [Core Concepts](./#nodes) for a breakdown of node categories and
[Core Concepts](./#data-types) for the supported data types.

---

## Next steps

- [Macro Resolution](macros) -- How macro substitution works under the hood.
- [Custom Templates](../guides/custom-templates) -- Write your own reusable templates.
- [Node Reference](../reference/nodes/) -- Full documentation for all node types.
