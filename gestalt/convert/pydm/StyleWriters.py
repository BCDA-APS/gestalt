from gestalt.Type import *

def style_textentry(node):
	stylesheet = """\
{my_class}#{my_name}
{{
    padding: 0px 0px 0px 2px; 
    border: 2px; 
    padding: 0px;
    border-style:inset; 
    border-color: rgba(43, 101, 114, 255) rgba(185, 242, 255, 255)  rgba(185, 242, 255, 255) rgba(43, 101, 114, 255);
}}
""".format(my_class=node.classname, my_name=node.name)
	return stylesheet
	
def style_button(node):
	col = Color(node["background"]).val()
	
	r = col["red"]
	g = col["green"]
	b = col["blue"]
	
	dr = int(r/255.0 * 170)
	dg = int(g/255.0 * 170)
	db = int(b/255.0 * 170)
	
	lr = int(min(1.2 * r, 255))
	lg = int(min(1.2 * g, 255))
	lb = int(min(1.2 * b, 255))

	stylesheet = """\
{my_class}#{my_name}
{{
	border-color: rgba({dr}, {dg}, {db}, 255);
	border-radius: 1px; 
	padding: 0px; 
	border-width: 3px;
	border-style: outset; 
	margin:0px
}}
{my_class}#{my_name}:pressed
{{
	background-color: rgba({dr}, {dg}, {db}, 255);
}}
{my_class}#{my_name}:hover
{{
	background-color: rgba({lr}, {lg}, {lb}, 255);
}}
""".format(
	my_class=node.classname, 
	my_name=node.name,
	dr = dr,
	dg = dg,
	db = db,
	lr = lr,
	lg = lg,
	lb = lb)
	
	node.toRemove.append("background")
	return stylesheet

def write_frameborder(node):
	stylesheet = ""
						
	col = Color(node["border-color"]).val()
	wid = Number(node["border-width"]).val()
	style = String(node["border-style"]).val()
		
	if (int(wid) != 0) and (col["alpha"] != 0):
		stylesheet += """
{my_class}#{my_name}
{{
    border-width: {width}px;
    border-style: {style};
    border-color: rgba({red},{green},{blue},{alpha});
}}
""".format(
		red=col["red"],
		green=col["green"],
		blue=col["blue"],
		alpha=col["alpha"],
		width=wid,
		style=style.lower(),
		my_name=node.name,
		my_class=node.classname)

	node.toRemove.append("border-color")
	node.toRemove.append("border-width")
	node.toRemove.append("border-style")

	return stylesheet

		
def write_color(node):
	background = node["background"]
	text_color = node["foreground"]
	
	stylesheet = """\
{my_class}#{my_name}
{{    
    background: rgba({br},{bg},{bb},{ba});
    color: rgba({tr},{tg},{tb},{ta});
}}
""".format(
	my_class = node.classname,
	my_name = node.name,
	br = int(background["red"]),
	bg = int(background["green"]),
	bb = int(background["blue"]),
	ba = int(background["alpha"]),
	tr = int(text_color["red"]),
	tg = int(text_color["green"]),
	tb = int(text_color["blue"]),
	ta = int(text_color["alpha"]))
	
	node.toRemove.append("background")
	node.toRemove.append("foreground")
	
	return stylesheet
		
def write_font(node):
	the_font = node["font"]
		
	style = the_font["style"].lower()
		
	if "regular" in style:
		style = ""
		
	align = str(node["alignment"])
		
	frame_align = "center"
		
	if "AlignLeft" in align:
		frame_align = "left"
	elif "AlignRight" in align:
		frame_align = "right"
					
	stylesheet = """\
{my_class}#{my_name}
{{
    font-family: {family};
    font: {style} {size}pt;
	
    text-align: {lcr};
}}
""".format(
	my_class = node.classname,
	my_name = node.name,
	family = the_font["family"],
	style  = style,
	size   = the_font["size"],
	lcr    = frame_align)
	
	node.toRemove.append("font")
	node.toRemove.append("alignment")
	return stylesheet
