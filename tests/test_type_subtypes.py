import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gestalt.Type import Rect, Color, Font, Alignment, List, Dict, String


class TestRect(unittest.TestCase):
	def test_four_components(self):
		r = Rect("10x20x100x200")
		v = r.val()
		self.assertEqual(v["x"], 10)
		self.assertEqual(v["y"], 20)
		self.assertEqual(v["width"], 100)
		self.assertEqual(v["height"], 200)

	def test_two_components_padded(self):
		r = Rect("100x200")
		v = r.val()
		self.assertEqual(v["x"], 0)
		self.assertEqual(v["y"], 0)
		self.assertEqual(v["width"], 100)
		self.assertEqual(v["height"], 200)

	def test_one_component_padded(self):
		r = Rect("100")
		v = r.val()
		self.assertEqual(v["x"], 0)
		self.assertEqual(v["y"], 0)
		self.assertEqual(v["width"], 0)
		self.assertEqual(v["height"], 100)

	def test_dict_input(self):
		r = Rect({"x": 5, "y": 10, "width": 100, "height": 200})
		v = r.val()
		self.assertEqual(int(v["x"]), 5)
		self.assertEqual(int(v["width"]), 100)

	def test_dict_missing_keys_default_zero(self):
		r = Rect({"width": 50})
		v = r.val()
		self.assertEqual(v["x"], 0)
		self.assertEqual(v["y"], 0)
		self.assertEqual(v["height"], 0)

	def test_updates_applied(self):
		r = Rect("10x20x100x200")
		r["width"] = 999
		v = r.val()
		self.assertEqual(v["width"], 999)

	def test_getitem_returns_int(self):
		r = Rect("10x20x100x200")
		self.assertIsInstance(r["x"], int)
		self.assertEqual(r["x"], 10)

	def test_str_roundtrip(self):
		r = Rect("10x20x100x200")
		self.assertEqual(str(r), "10x20x100x200")

	def test_with_macros(self):
		r = Rect("{W}x{H}")
		r.apply({"W": "50", "H": "30"})
		v = r.val()
		self.assertEqual(v["width"], 50)
		self.assertEqual(v["height"], 30)

	def test_geometry_with_spaces(self):
		# "XxY x WxH" format sometimes used
		r = Rect("0x0 x 100x200")
		# After macro resolution, spaces are part of the string
		# The split by 'x' should still work
		v = r.val()
		self.assertEqual(v["width"], 100)
		self.assertEqual(v["height"], 200)


class TestColor(unittest.TestCase):
	def test_four_component_with_dollar(self):
		c = Color("$FF00FF80")
		v = c.val()
		self.assertEqual(v["red"], 255)
		self.assertEqual(v["green"], 0)
		self.assertEqual(v["blue"], 255)
		self.assertEqual(v["alpha"], 128)

	def test_three_component_alpha_default(self):
		c = Color("$FF0000")
		v = c.val()
		self.assertEqual(v["red"], 255)
		self.assertEqual(v["green"], 0)
		self.assertEqual(v["blue"], 0)
		self.assertEqual(v["alpha"], 255)

	def test_transparent(self):
		c = Color("$00000000")
		v = c.val()
		self.assertEqual(v["alpha"], 0)

	def test_dict_input(self):
		c = Color({"red": 100, "green": 150, "blue": 200, "alpha": 255})
		v = c.val()
		self.assertEqual(v["red"], 100)
		self.assertEqual(v["alpha"], 255)

	def test_str_format(self):
		c = Color("$FF00FF80")
		self.assertEqual(str(c), "$FF00FF80")

	def test_str_three_component(self):
		c = Color("$FF0000")
		self.assertEqual(str(c), "$FF0000FF")

	def test_updates(self):
		c = Color("$FF000000")
		c["alpha"] = 128
		v = c.val()
		self.assertEqual(v["alpha"], 128)

	def test_nearly_transparent(self):
		c = Color("$00000001")
		v = c.val()
		self.assertEqual(v["alpha"], 1)


class TestFont(unittest.TestCase):
	def test_standard_with_leading_dash(self):
		f = Font("-Liberation Sans-Bold-12")
		v = f.val()
		self.assertEqual(v["family"], "Liberation Sans")
		self.assertEqual(v["style"], "Bold")
		self.assertEqual(v["size"], "12")

	def test_dict_input(self):
		f = Font({"family": "Arial", "style": "Regular", "size": "14"})
		v = f.val()
		self.assertEqual(v["family"], "Arial")
		self.assertEqual(v["size"], "14")

	def test_with_macros(self):
		f = Font("-{fontname}-Bold-{fontsize}")
		f.apply({"fontname": "Courier", "fontsize": "10"})
		v = f.val()
		self.assertEqual(v["family"], "Courier")
		self.assertEqual(v["size"], "10")

	def test_updates(self):
		f = Font("-Arial-Regular-12")
		f["size"] = "16"
		v = f.val()
		self.assertEqual(v["size"], "16")


class TestAlignment(unittest.TestCase):
	def test_top_left(self):
		a = Alignment("TopLeft")
		v = a.val()
		self.assertEqual(v["vertical"], "Top")
		self.assertEqual(v["horizontal"], "Left")

	def test_center(self):
		a = Alignment("Center")
		v = a.val()
		self.assertEqual(v["vertical"], "Center")
		self.assertEqual(v["horizontal"], "Center")

	def test_bottom_right(self):
		a = Alignment("BottomRight")
		v = a.val()
		self.assertEqual(v["vertical"], "Bottom")
		self.assertEqual(v["horizontal"], "Right")

	def test_top_only(self):
		a = Alignment("Top")
		v = a.val()
		self.assertEqual(v["vertical"], "Top")
		self.assertEqual(v["horizontal"], "Center")

	def test_right_only(self):
		a = Alignment("Right")
		v = a.val()
		self.assertEqual(v["vertical"], "Center")
		self.assertEqual(v["horizontal"], "Right")

	def test_case_insensitive(self):
		a = Alignment("topleft")
		v = a.val()
		self.assertEqual(v["vertical"], "Top")
		self.assertEqual(v["horizontal"], "Left")

	def test_center_right(self):
		a = Alignment("CenterRight")
		v = a.val()
		self.assertEqual(v["vertical"], "Center")
		self.assertEqual(v["horizontal"], "Right")

	def test_dict_input(self):
		a = Alignment({"vertical": "bottom", "horizontal": "left"})
		v = a.val()
		self.assertEqual(v["vertical"], "Bottom")
		self.assertEqual(v["horizontal"], "Left")

	def test_str_concatenates(self):
		a = Alignment("TopLeft")
		self.assertEqual(str(a), "TopLeft")

	def test_middle_center(self):
		a = Alignment("MiddleCenter")
		v = a.val()
		self.assertEqual(v["vertical"], "Center")
		self.assertEqual(v["horizontal"], "Center")


class TestListType(unittest.TestCase):
	def test_from_python_list(self):
		l = List([1, 2, 3])
		v = l.val()
		self.assertEqual(v, ["1", "2", "3"])

	def test_from_json_like_string(self):
		l = List("[1, 2, 3]")
		v = l.val()
		self.assertIsInstance(v, list)
		self.assertEqual(len(v), 3)

	def test_with_macros(self):
		l = List(["{X}", "{Y}"])
		l.apply({"X": "a", "Y": "b"})
		v = l.val()
		self.assertEqual(v, ["a", "b"])

	def test_iteration(self):
		l = List(["a", "b", "c"])
		result = [item for item in l]
		self.assertEqual(len(result), 3)

	def test_str_representation(self):
		l = List([1, 2, 3])
		s = str(l)
		self.assertIsInstance(s, str)

	def test_from_string_list(self):
		l = List(["hello", "world"])
		v = l.val()
		self.assertEqual(v, ["hello", "world"])


class TestDictType(unittest.TestCase):
	def test_from_python_dict(self):
		d = Dict({"a": 1, "b": 2})
		v = d.val()
		self.assertEqual(v["a"], "1")
		self.assertEqual(v["b"], "2")

	def test_from_json_like_string(self):
		d = Dict("{a: 1, b: 2}")
		v = d.val()
		self.assertIsInstance(v, dict)
		self.assertIn("a", v)

	def test_with_macros(self):
		d = Dict({"key": "{name}"})
		d.apply({"name": "resolved"})
		v = d.val()
		self.assertEqual(v["key"], "resolved")

	def test_iteration(self):
		d = Dict({"a": 1, "b": 2})
		keys = [k for k in d]
		self.assertIn("a", keys)
		self.assertIn("b", keys)

	def test_str_representation(self):
		d = Dict({"a": 1})
		s = str(d)
		self.assertIsInstance(s, str)

	def test_nested_dict_values(self):
		d = Dict({"outer": "{inner: value}"})
		v = d.val()
		# The json_like guard prevents non-json-like strings from being parsed
		# "{inner: value}" IS json_like so it gets parsed
		self.assertIsInstance(v["outer"], dict)

	def test_non_json_like_string_stays_string(self):
		d = Dict({"macros": "P=1,R=A"})
		v = d.val()
		self.assertIsInstance(v["macros"], str)

	def test_colon_in_value_not_parsed(self):
		# Strings containing ": " (colon-space) look like YAML key-value
		# pairs but should NOT be parsed when not wrapped in braces
		d = Dict({"macros": "P=prefix:,DESC=Label: Description"})
		v = d.val()
		self.assertIsInstance(v["macros"], str)


if __name__ == "__main__":
	unittest.main()
