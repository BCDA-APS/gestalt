---
layout: default
title: Build Integration
parent: Guides
nav_order: 7
---

# Build Integration
{: .no_toc}

## Table of contents
{: .no_toc .text-delta }

- TOC
{:toc}

Gestalt integrates with Make-based build systems to automatically regenerate screens
when layout files or input data change.


## Basic Makefile rule

A simple rule that generates a screen from a layout and data file:

```makefile
GESTALT = python /path/to/gestalt.py

screen.ui: layout.yml data.yml
    $(GESTALT) --to ui --input data.yml --output $@ layout.yml
```

This works but requires you to manually list every dependency. If `layout.yml` includes
other files (like `colors.yml` or template files), changes to those included files will
not trigger a rebuild.


## Automatic dependency tracking

Gestalt can output a list of all files that a layout depends on, including every file
pulled in by `#include` statements. Use the `--depends` flag:

```bash
python gestalt.py --depends --input data.yml layout.yml
```

This prints a Make-compatible dependency list to stdout:

```
layout.ui: layout.yml data.yml colors.yml widgets.yml on-off.yml read-write.yml ...
```

Use this to generate dependency files that Make can include:

```makefile
GESTALT = python /path/to/gestalt.py
LAYOUTS = screen1 screen2 screen3

# Generate .ui files
%.ui: %.yml
    $(GESTALT) --to ui --input $*_data.yml --output $@ $<

# Generate dependency files
.depends/%.ui.d: %.yml
    @mkdir -p .depends
    $(GESTALT) --depends --input $*_data.yml $< > $@

# Include dependency files (if they exist)
-include $(LAYOUTS:%=.depends/%.ui.d)
```

With this setup:
1. The first build generates both the `.ui` file and a `.d` dependency file.
2. On subsequent builds, Make reads the `.d` file and knows every included file.
3. If any included file changes, the screen is automatically regenerated.


## Multiple output formats

Generate both caQtDM and Phoebus output from the same layout:

```makefile
GESTALT = python /path/to/gestalt.py

SCREENS = device status motors

QT_SCREENS  = $(SCREENS:%=%.ui)
CSS_SCREENS = $(SCREENS:%=%.bob)

all: $(QT_SCREENS) $(CSS_SCREENS)

%.ui: %.yml %_data.yml
    $(GESTALT) --to ui --input $*_data.yml --output $@ $<

%.bob: %.yml %_data.yml
    $(GESTALT) --to bob --input $*_data.yml --output $@ $<
```


## Shared include directories

If your template files live in a shared location, pass the directory with `--include`:

```makefile
GESTALT = python /path/to/gestalt.py
TEMPLATE_DIR = /path/to/shared/templates

%.ui: %.yml
    $(GESTALT) --include $(TEMPLATE_DIR) --to ui --input $*_data.yml --output $@ $<
```

Multiple `--include` flags can be specified:

```makefile
GESTALT_FLAGS = --include $(TEMPLATE_DIR) --include $(SITE_DIR)

%.ui: %.yml
    $(GESTALT) $(GESTALT_FLAGS) --to ui --input $*_data.yml --output $@ $<
```


## Integration with EPICS build system

For EPICS IOC applications, screen generation can be added to the IOC's Makefile. A
typical pattern places layouts in an `op/` or `screens/` directory:

```makefile
# screens/Makefile

GESTALT = python $(TOP)/support/gestalt/gestalt.py
WIDGET_DIR = $(TOP)/support/gestalt/widgets

SCREENS = ioc_status motor_control

all: $(SCREENS:%=%.ui) $(SCREENS:%=%.bob)

%.ui: %.yml %_data.yml
    $(GESTALT) --include $(WIDGET_DIR) --to ui --input $*_data.yml --output $@ $<

%.bob: %.yml %_data.yml
    $(GESTALT) --include $(WIDGET_DIR) --to bob --input $*_data.yml --output $@ $<

clean:
    rm -f *.ui *.bob
```

---

## Next steps

- [Architecture](../concepts/architecture) -- How Gestalt processes layout files internally.
- [Command Line Options](../reference/commandline) -- Full command-line option reference.
