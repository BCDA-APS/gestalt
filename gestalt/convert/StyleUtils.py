from gestalt.Type import Color, Number, String


def _rgba(color):
	"""Format a color dict as an rgba() CSS value string."""
	return "rgba({},{},{},{})".format(
		int(color["red"]), int(color["green"]),
		int(color["blue"]), int(color["alpha"]))


def qss_border(selector, color, width, style="solid"):
	"""Generate a CSS border rule.
	
	Returns an empty string if the border is invisible (width 0 or fully transparent).
	
	Args:
		selector: CSS selector string (e.g., "QFrame", "MyClass#myName")
		color:    Color dict with red, green, blue, alpha keys
		width:    Border width in pixels
		style:    Border style string (default "solid")
	"""
	if int(width) == 0 or int(color["alpha"]) == 0:
		return ""
	
	return """\
{selector}
{{
    border-width: {width}px;
    border-style: {style};
    border-color: {rgba};
}}
""".format(selector=selector, width=width, style=style.lower(), rgba=_rgba(color))


def qss_font(selector, font):
	"""Generate a CSS font rule.
	
	Args:
		selector: CSS selector string
		font:     A dict (or Font object) with family, style, and optionally size keys
	"""
	# Resolve Font objects to plain dicts
	if hasattr(font, "val"):
		font = font.val()
	
	style = (font.get("style") or "").lower()
	
	if "regular" in style:
		style = ""
	
	size_str = ""
	size = font.get("size")
	if size:
		size_str = " {}pt".format(size)
	
	return """\
{selector}
{{
    font-family: {family};
    font: {style}{size};
}}
""".format(selector=selector, family=font["family"], style=style, size=size_str)


def qss_color(selector, background, foreground):
	"""Generate CSS background and text color rules.
	
	Args:
		selector:   CSS selector string
		background: Color dict for background
		foreground: Color dict for text color
	"""
	return """\
{selector}
{{
    background: {bg};
    color: {fg};
}}
""".format(selector=selector, bg=_rgba(background), fg=_rgba(foreground))


def qss_textentry(selector):
	"""Generate CSS for text entry inset border styling.
	
	Args:
		selector: CSS selector string
	"""
	return """\
{selector}
{{
    border: 2px;
    padding: 0px;
    border-style:inset;
    border-color: rgba(43, 101, 114, 255) rgba(185, 242, 255, 255)  rgba(185, 242, 255, 255) rgba(43, 101, 114, 255);
}}
""".format(selector=selector)


def qss_button(selector, color):
	"""Generate CSS for a button with pressed/hover state variants.
	
	Computes darker (pressed) and lighter (hover) variants from the base color.
	
	Args:
		selector: CSS selector string
		color:    Color dict for the button background
	"""
	r = color["red"]
	g = color["green"]
	b = color["blue"]
	
	dr = int(r / 255.0 * 170)
	dg = int(g / 255.0 * 170)
	db = int(b / 255.0 * 170)
	
	lr = int(min(1.2 * r, 255))
	lg = int(min(1.2 * g, 255))
	lb = int(min(1.2 * b, 255))
	
	return """\
{selector}
{{
	border-color: rgba({dr}, {dg}, {db}, 255);
	border-radius: 1px;
	padding: 0px;
	border-width: 3px;
	border-style: outset;
	margin:0px
}}
{selector}:pressed
{{
	background-color: rgba({dr}, {dg}, {db}, 255);
}}
{selector}:hover
{{
	background-color: rgba({lr}, {lg}, {lb}, 255);
}}
""".format(selector=selector, dr=dr, dg=dg, db=db, lr=lr, lg=lg, lb=lb)


def qss_selected(selector, color):
	"""Generate CSS for a selected/checked QPushButton state.
	
	Args:
		selector: CSS selector string (the checked rule is appended)
		color:    Color dict for the selected background
	"""
	return """\
{selector} QPushButton:checked
{{
    background-color: {rgba};
}}
""".format(selector=selector, rgba=_rgba(color))


def qss_tabbed_group(node):
	"""Generate the full tabbed group stylesheet.
	
	Pops the following properties from the node: inset, tab-color, foreground,
	padding, offset, border-width, border-color, border-style, selected, background.
	Reads (without popping): font, tabbar-height.
	
	Args:
		node: A widget node with tabbed group properties
	"""
	stylesheet = ""
	
	tab_offset = node.pop("inset")
	
	stylesheet += """\
QTabWidget::tab-bar
{{
    left: {inset}px;
}}

""".format(inset=int(tab_offset))
	
	the_font = node["font"].val()
	
	tab_color      = node.pop("tab-color")
	font_color     = node.pop("foreground")
	tab_padding    = node.pop("padding")
	content_offset = node.pop("offset")
	
	stylesheet += """\
QTabBar::tab
{{
    margin-right: {margin}px;
    margin-bottom: {offset}px;
	
    padding-top: 0px;
    padding-bottom: 0px;
    padding-left: 5px;
    padding-right: 5px;
    
    height: {tab_height}px;
	
    background: {tab_bg};
    color: {tab_fg};
}}

QTabBar::tab:hover
{{
    color: {tab_bg};
    background: {tab_fg};
}}

""".format(
	margin=int(tab_padding),
	offset=int(content_offset),
	tab_height=int(node["tabbar-height"]) - int(content_offset),
	tab_bg=_rgba(tab_color),
	tab_fg=_rgba(font_color))
	
	border_width = node.pop("border-width")
	border_color = node.pop("border-color")
	border_style = node.pop("border-style")
	
	stylesheet += """\
QTabWidget::pane
{{
    border-style: {style};
    border-width: {width}px;
    border-color: {rgba};
}}

""".format(
	width=int(border_width),
	rgba=_rgba(border_color),
	style=str(border_style).lower())
	
	select_color = node.pop("selected")
	
	stylesheet += """\
QTabBar::tab:selected
{{
    background: {rgba};
}}

""".format(rgba=_rgba(select_color))
	
	background = node.pop("background")
	
	stylesheet += """\
QWidget[Fill="True"] 
{{ 
    background: {rgba};
}}
""".format(rgba=_rgba(background))
	
	return stylesheet
