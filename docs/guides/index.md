---
layout: default
title: Guides
nav_order: 4
has_children: true
has_toc: false
---

# Guides
{: .no_toc}

Goal-oriented guides for common tasks.

---

### Getting set up

- [Installation](installation) -- Prerequisites, dependencies, and verifying your setup.

### Layout techniques

- [Using Data Files](data-files) -- Provide input data in YAML, JSON, substitutions, or INI format.
- [Data-Driven Layouts](repeat-and-grid) -- Generate repeated widgets from data lists, counts, or grids.

### Writing templates

- [Custom Templates](custom-templates) -- Write your own reusable widget groups with `!Template` and `!Apply`.
- [Conditional Elements](conditionals) -- Optionally show or hide elements with `!If` and `!IfNot`.
- [Overridable Elements](embed-override) -- Let callers replace entire widgets using `!Embed`.

### Build system

- [Build Integration](build-integration) -- Makefile patterns and automatic dependency tracking.
