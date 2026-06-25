# PyDM-specific adapters for the shared QSS utilities in StyleUtils.
# Each function constructs a scoped CSS selector from the node, delegates
# to the corresponding StyleUtils function for QSS generation, and manages
# the node's toRemove list for property cleanup during write.

from gestalt.Type import *
from gestalt.convert.StyleUtils import qss_textentry, qss_button, qss_border, qss_color, qss_font, qss_selected


def style_textentry(node):
	selector = "{}#{}".format(node.classname, node.name)
	return qss_textentry(selector)


def style_button(node):
	selector = "{}#{}".format(node.classname, node.name)
	col = Color(node["background"]).val()

	stylesheet = qss_button(selector, col)

	node.toRemove.append("background")
	return stylesheet


def write_frameborder(node):
	selector = "{}#{}".format(node.classname, node.name)
	col = Color(node["border-color"]).val()
	wid = Number(node["border-width"]).val()
	style = String(node["border-style"]).val()

	stylesheet = qss_border(selector, col, wid, style)

	node.toRemove.append("border-color")
	node.toRemove.append("border-width")
	node.toRemove.append("border-style")

	return stylesheet


def write_color(node):
	selector = "{}#{}".format(node.classname, node.name)
	background = node["background"]
	foreground = node["foreground"]

	stylesheet = qss_color(selector, background, foreground)

	node.toRemove.append("background")
	node.toRemove.append("foreground")

	return stylesheet


def write_font(node):
	selector = "{}#{}".format(node.classname, node.name)
	the_font = node["font"]

	stylesheet = qss_font(selector, the_font)

	node.toRemove.append("font")

	if "alignment" in node:
		node.toRemove.append("alignment")

	return stylesheet


def style_selected(node):
	if "selected" not in node:
		return ""

	selector = "{}#{}".format(node.classname, node.name)
	col = Color(node["selected"]).val()

	stylesheet = qss_selected(selector, col)

	node.toRemove.append("selected")
	return stylesheet
