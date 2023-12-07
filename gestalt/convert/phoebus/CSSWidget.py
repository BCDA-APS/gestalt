from gestalt.Type import *

from gestalt.Node import GroupNode

from phoebusgen import widget
from phoebusgen.widget import properties as _p

name_numbering = {}

class CSSWidget(GroupNode):
	def __init__(self, classname, name=None, layout={}, macros={}):
		super(CSSWidget, self).__init__(classname, name=name, layout=layout)
		
		self.macros = macros
		
		if name:
			self.name = name
		else:
			num = name_numbering.get(classname, 0)
			num += 1
			name_numbering[classname] = num
			
			self.name = classname + str(num)
			
		if   (self.classname == "ActionButton"):
			self.widget = widget.ActionButton(self.name, "", "", 0, 0, 0, 0)
		elif (self.classname == "Arc"):
			self.widget = widget.Arc(self.name, 0, 0, 0, 0)
		elif (self.classname == "Array"):
			self.widget = widget.Array(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "BooleanButton"):
			self.widget = widget.BooleanButton(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "ByteMonitor"):
			self.widget = widget.ByteMonitor(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "CheckBox"):
			self.widget = widget.CheckBox(self.name, "", "", 0, 0, 0, 0)
		elif (self.classname == "ChoiceButton"):
			self.widget = widget.ChoiceButton(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "ComboBox"):
			self.widget = widget.ComboBox(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "DataBrowser"):
			self.widget = widget.DataBrowser(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Ellipse"):
			self.widget = widget.Ellipse(self.name, 0, 0, 0, 0)
		elif (self.classname == "EmbeddedDisplay"):
			self.widget = widget.EmbeddedDisplay(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "FileSelector"):
			self.widget = widget.FileSelector(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Group"):
			self.widget = widget.Group(self.name, 0, 0, 0, 0)
		elif (self.classname == "Image"):
			self.widget = widget.Image(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "LED"):
			self.widget = widget.LED(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "LEDMultiState"):
			self.widget = widget.LEDMultiState(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Label"):
			self.widget = widget.Label(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Meter"):
			self.widget = widget.Meter(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "NavigationTabs"):
			self.widget = widget.NavigationTabs(self.name, 0, 0, 0, 0)
		elif (self.classname == "Picture"):
			self.widget = widget.Picture(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Polygon"):
			self.widget = widget.Polygon(self.name, 0, 0, 0, 0)
		elif (self.classname == "Polyline"):
			self.widget = widget.Polylin(self.name, 0, 0, 0, 0)
		elif (self.classname == "ProgressBar"):
			self.widget = widget.ProgressBar(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "RadioButton"):
			self.widget = widget.RadioButton(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Rectangle"):
			self.widget = widget.Rectangle(self.name, 0, 0, 0, 0)
		elif (self.classname == "ScaledSlider"):
			self.widget = widget.ScaledSlider(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Scrollbar"):
			self.widget = widget.Scrollbar(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "SlideButton"):
			self.widget = widget.SlideButton(self.name, "", "", 0, 0, 0, 0)
		elif (self.classname == "Spinner"):
			self.widget = widget.Spinner(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "StripChart"):
			self.widget = widget.StripChart(self.name, 0, 0, 0, 0)
		elif (self.classname == "Symbol"):
			self.widget = widget.Symbol(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Table"):
			self.widget = widget.Table(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Tabs"):
			self.widget = widget.Tabs(self.name, 0, 0, 0, 0)
		elif (self.classname == "Tank"):
			self.widget = widget.Tank(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "TextEntry"):
			self.widget = widget.TextEntry(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "TextSymbol"):
			self.widget = widget.TextSymbol(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "TextUpdate"):
			self.widget = widget.TextUpdate(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "Thermometer"):
			self.widget = widget.Thermometer(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "ThreeDViewer"):
			self.widget = widget.ThreeDViewer(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "WebBrowser"):
			self.widget = widget.WebBrowser(self.name, "", 0, 0, 0, 0)
		elif (self.classname == "XYPlot"):
			self.widget = widget.XYPlot(self.name, 0, 0, 0, 0)	
		else:
			raise Exception("Unknown widget type: " + self.classname)
			
	def setBasicParam(self, set_fun, attribute, check_class=object):
		if isinstance(self.widget, check_class) and attribute in self.attrs:
			getattr(self.widget, set_fun)(self[attribute].val)

	def setColorParam(self, set_fun, attribute, check_class=object):
		if isinstance(self.widget, check_class):
			col = None
			
			if attribute + "_color" in self.attrs:
				col = self[attribute + "_color"]
			elif attribute in self.attrs:
				col = self[attribute]
			else:
				return
			
			if isinstance(col, Color):
				getattr(self.widget, set_fun)(col.val["red"], col.val["green"], col.val["blue"], col.val["alpha"])
			elif isinstance(col, String):
				getattr(self.widget, "predefined_" + set_fun)(col.val)
		
	def setEnumParam(self, set_fun, attribute, enum_class, check_class=object):
		if isinstance(self.widget, check_class) and attribute in self.attrs:
			enumer = self[attribute]
			
			if isinstance(enumer, Number):
				# self.widget.<function>(<enumeration>(<given value>))
				getattr(self.widget, set_fun)(getattr(self.widget._shared, enum_class)(int(enumer.val)))
			elif isinstance(enumer, String):
				# self.widget.<function>((getattr(<enumeration>, <given value>)
				getattr(self.widget, set_fun)(getattr(getattr(self.widget._shared, enum_class), enumer.val.lower()))
			
	def setFontParam(self, attribute, prefix, check_class=object):
		if isinstance(self.widget, check_class):
			my_font = None
			
			if attribute + "_font" in self.attrs:
				my_font = self[attribute + "_font"]
			elif attribute in self.attrs:
				my_font = self[attribute]
			else:
				return
				
			getattr(self.widget, prefix + "font_family")(my_font["family"])
				
			if my_font["size"]:
				getattr(self.widget, prefix + "font_size")(int(my_font["size"]))
				
			if my_font["style"]:
				getattr(self.widget, prefix + "font_style_" + my_font["style"])()
				
		
	def write(self, screen):
		for key, item in self.attrs.items():
			item.apply(self.macros)
			
		if self.widget:
			self.widget.name(self.name)
			self.widget.x(self["geometry"]["x"])
			self.widget.y(self["geometry"]["y"])
			self.widget.width(self["geometry"]["width"])
			self.widget.height(self["geometry"]["height"])
			
			
			##############
			#  Booleans  #
			##############
			
			self.setBasicParam("visible",  "visible")
			self.setBasicParam("tool_tip", "tool_tip")
		 	
			self.setBasicParam("auto_size",        "auto_size",          check_class=_p._AutoSize)
			self.setBasicParam("auto_scale",       "auto_scale",         check_class=_p._AutoScale)
			self.setBasicParam("transparent",      "transparent",        check_class=_p._Transparent)
			self.setBasicParam("show_units",       "show_units",         check_class=_p._ShowUnits)
			self.setBasicParam("wrap_words",       "wrap_words",         check_class=_p._WrapWords)
			self.setBasicParam("square",           "square",             check_class=_p._Square)
			self.setBasicParam("editable",         "editable",           check_class=_p._Editable)
			self.setBasicParam("items_from_pv",    "items_from_pv",      check_class=_p._ItemsFromPV)
			self.setBasicParam("labels_from_pv",   "labels_from_pv",     check_class=_p._LabelsFromPV)
			self.setBasicParam("limits_from_pv",   "limits_from_pv",     check_class=_p._LimitsFromPV)
			self.setBasicParam("enabled",          "enabled",            check_class=_p._Enabled)
			self.setBasicParam("multiline",        "multiline",          check_class=_p._MultiLine)
			self.setBasicParam("stretch_to_fit",   "stretch_image",      check_class=_p._StretchToFit)
			self.setBasicParam("horizontal",       "horizontal",         check_class=_p._Horizontal)
			self.setBasicParam("show_led",         "show_led",           check_class=_p._ShowLED)
			self.setBasicParam("show_grid",        "show_grid",          check_class=_p._ShowGrid)
			self.setBasicParam("show_limits",      "show_limits",        check_class=_p._ShowLimits)
			self.setBasicParam("show_index",       "show_index",         check_class=_p._ShowIndex)
			self.setBasicParam("show_value",       "show_value",         check_class=_p._ShowValue)
			self.setBasicParam("show_scale",       "show_scale",         check_class=_p._ShowScale)
			self.setBasicParam("show_legend",      "show_legend",        check_class=_p._ShowLegend)
			self.setBasicParam("show_value_tip",   "show_value_tip",     check_class=_p._ShowValueTip)
			self.setBasicParam("show_minor_ticks", "show_minor_ticks",   check_class=_p._ShowMinorTicks)
			self.setBasicParam("show_toolbar",     "show_toolbar",       check_class=_p._ShowToolbar)
			self.setBasicParam("scale_visible",    "scale_visible",      check_class=_p._ScaleVisible)
			self.setBasicParam("reverse_bits",     "bitReverse",         check_class=_p._ReverseBits)
			self.setBasicParam("preserve_ratio",   "preserve_ratio",     check_class=_p._PreserveRatio)
			self.setBasicParam("select_rows",      "row_selection_mode", check_class=_p._SelectRows)
			self.setBasicParam("unsigned_data",    "unsigned",           check_class=_p._UnsignedData)
			self.setBasicParam("log_scale",        "log_scale",          check_class=_p._LogScale)
			self.setBasicParam("show_hihi",        "show_hihi",          check_class=_p._LevelsAndShow)
			self.setBasicParam("show_high",        "show_high",          check_class=_p._LevelsAndShow)
			self.setBasicParam("show_low",         "show_low",           check_class=_p._LevelsAndShow)
			self.setBasicParam("show_lolo",        "show_lolo",          check_class=_p._LevelsAndShow)
			self.setBasicParam("cursor_crosshair", "cursor_crosshair",   check_class=_p._Cursor)
			
			
			self.setBasicParam("buttons_on_left", "buttons_on_left",           check_class=_p._ButtonsOnLeft)
			self.setBasicParam("alarm_border",    "border_alarm_sensitive",    check_class=_p._AlarmBorder)
				
			#############
			#  Strings  #
			#############
								
			self.setBasicParam("pv_name",        "pv_name",        check_class=_p._PVName)
			self.setBasicParam("tab",            "tab",            check_class=_p._Tabs)
			self.setBasicParam("text",           "text",           check_class=_p._Text)
			self.setBasicParam("format",         "format",         check_class=_p._Format)
			self.setBasicParam("title",          "title",          check_class=_p._Title)
			self.setBasicParam("time_range",     "time_range",     check_class=_p._TimeRange)
			self.setBasicParam("scale_format",   "scale_format",   check_class=_p._ScaleFormat)
			self.setBasicParam("off_label",      "off_label",      check_class=_p._Off)
			self.setBasicParam("off_image",      "off_image",      check_class=_p._OffImage)
			self.setBasicParam("on_label",       "on_label",       check_class=_p._On)
			self.setBasicParam("on_image",       "on_image",       check_class=_p._OnImage)
			self.setBasicParam("url",            "url",            check_class=_p._URL)
			self.setBasicParam("file",           "file",           check_class=_p._File)
			self.setBasicParam("label",          "label",          check_class=_p._Label)
			self.setBasicParam("group_name",     "group_name",     check_class=_p._GroupName)
			self.setBasicParam("selection_pv",   "selection_pv",   check_class=_p._SelectionPV)
			self.setBasicParam("fallback_label", "fallback_label", check_class=_p._Fallback)  
			self.setBasicParam("cursor_info_pv", "cursor_info_pv", check_class=_p._Cursor)
			self.setBasicParam("cursor_x_pv",    "x_pv",           check_class=_p._Cursor)
			self.setBasicParam("cursor_y_pv",    "y_pv",           check_class=_p._Cursor)
			
			self.setBasicParam("selection_value_pv", "selection_value_pv", check_class=_p._SelectionValuePV)
			
			#############
			#  Numbers  #
			#############
				
			self.setBasicParam("precision",     "precision",     check_class=_p._Precision)
			self.setBasicParam("bit",           "bit",           check_class=_p._Bit)
			self.setBasicParam("num_bits",      "numBits",       check_class=_p._NumBits)
			self.setBasicParam("start_bit",     "startBit",      check_class=_p._StartBit)
			self.setBasicParam("line_width",    "line_width",    check_class=_p._LineWidth)
			self.setBasicParam("rotation",      "rotation",      check_class=_p._Rotation)
			self.setBasicParam("bar_length",    "bar_length",    check_class=_p._BarLength)
			self.setBasicParam("increment",     "increment",     check_class=_p._Increment)
			self.setBasicParam("active_tab",    "active_tab",    check_class=_p._ActiveTab)
			self.setBasicParam("tab_height",    "tab_height",    check_class=_p._TabHeight)
			self.setBasicParam("tab_width",     "tab_width",     check_class=_p._TabWidth)
			self.setBasicParam("tab_spacing",   "tab_spacing",   check_class=_p._TabSpacing)
			self.setBasicParam("array_index",   "array_index",   check_class=_p._ArrayIndex)
			self.setBasicParam("initial_index", "initial_index", check_class=_p._InitialIndex)
			self.setBasicParam("border_width",  "border_width",  check_class=_p._Border)
			self.setBasicParam("corner_height", "corner_height", check_class=_p._Corner)
			self.setBasicParam("corner_width",  "corner_width",  check_class=_p._Corner)
			self.setBasicParam("angle_start",   "start_angle",   check_class=_p._Angle)
			self.setBasicParam("angle_size",    "total_angle",   check_class=_p._Angle)
			self.setBasicParam("data_height",   "data_height",   check_class=_p._Corner)
			self.setBasicParam("data_width",    "data_width",    check_class=_p._Corner)
			self.setBasicParam("minimum",       "minimum",       check_class=_p._MinMax)
			self.setBasicParam("maximum",       "maximum",       check_class=_p._MinMax)
			self.setBasicParam("level_hihi",    "level_hihi",    check_class=_p._LevelsAndShow)
			self.setBasicParam("level_high",    "level_high",    check_class=_p._LevelsAndShow)
			self.setBasicParam("level_low",     "level_low",     check_class=_p._LevelsAndShow)
			self.setBasicParam("level_lolo",    "level_lolo",    check_class=_p._LevelsAndShow)
			
			self.setBasicParam("major_ticks_pixel_dist", "major_tick_step_hint", check_class=_p._MajorTicksPixelDist)
				
			############
			#  Colors  #
			############
				
			self.setColorParam("foreground_color", "foreground", check_class=_p._ForegroundColor)
			self.setColorParam("background_color", "background", check_class=_p._BackgroundColor)
			self.setColorParam("on_color",         "on",         check_class=_p._OnColor)
			self.setColorParam("off_color",        "off",        check_class=_p._OffColor)
			self.setColorParam("needle_color",     "needle",     check_class=_p._NeedleColor)
			self.setColorParam("knob_color",       "knob",       check_class=_p._KnobColor)
			self.setColorParam("fill_color",       "fill",       check_class=_p._FillColor)
			self.setColorParam("empty_color",      "empty",      check_class=_p._EmptyColor)
			self.setColorParam("selected_color",   "selected",   check_class=_p._SelectedColor)
			self.setColorParam("deselected_color", "deselected", check_class=_p._DeselectedColor)
			self.setColorParam("grid_color",       "grid",       check_class=_p._GridColor)
			self.setColorParam("border_color",     "border",     check_class=_p._Border)
			self.setColorParam("fallback_color",   "fallback",   check_class=_p._Fallback)
			
			
			###########
			#  Enums  #
			###########
			
			self.setEnumParam("_add_horizontal_alignment", "horizontal_alignment", "HorizontalAlignment", check_class=_p._HorizontalAlignment)
			self.setEnumParam("_add_vertical_alignment",   "vertical_alignment",   "VerticalAlignment",   check_class=_p._VerticalAlignment)
			self.setEnumParam("_add_rotation_step",        "rotation_step",        "RotationStep",        check_class=_p._RotationStep)
			self.setEnumParam("_add_mode",                 "mode",                 "Mode",                check_class=_p._Mode)
			self.setEnumParam("_add_style",                "style",                "GroupStyle",          check_class=_p._Style)
			self.setEnumParam("_add_resize_behavior",      "resize",               "Resize",              check_class=_p._ResizeBehavior)
			self.setEnumParam("_add_file_component",       "component",            "FileComponent",       check_class=_p._FileComponent)
			self.setEnumParam("_add_interpolation",        "interpolation",        "Interpolation",       check_class=_p._Interpolation)			

			
			###########
			#  Fonts  #
			###########
			
			self.setFontParam("font",       "", check_class=_p._Font)
			self.setFontParam("title", "title_", check_class=_p._TitleFont)
			self.setFontParam("scale", "scale_", check_class=_p._ScaleFont)
			self.setFontParam("label", "label_", check_class=_p._LabelFont)
			
			
		for child in self.children:
			child.write(self.widget)
			
		screen.add_widget(self.widget)
