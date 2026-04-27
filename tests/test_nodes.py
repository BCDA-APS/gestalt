import unittest
import copy
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gestalt.Type import (
	DataType, String, Number, Double, Bool, Not, Color, Rect, Font, Alignment, List, Dict
)
from gestalt.nodes.Node import Node
from gestalt.nodes.GroupNode import GroupNode
from gestalt.nodes.FlowNode import FlowNode
from gestalt.nodes.RepeatNode import RepeatNode
from gestalt.nodes.LayoutNode import LayoutNode
from gestalt.nodes.CenterNode import CenterNode
from gestalt.nodes.ConditionalNode import ConditionalNode
from gestalt.nodes.ApplyNode import ApplyNode, _wrap_datatype
from gestalt.nodes.SpacerNode import SpacerNode
from gestalt.nodes.TextNode import TextNode
from gestalt.Generator import GestaltGenerator


class MockGenerator(GestaltGenerator):
	"""Minimal generator for testing node apply coroutines."""

	def generateGroup(self, original, macros=None):
		if macros is None:
			macros = {}
		output = GroupNode(node=original)
		output.updateProperties(macros)
		output.setDefault(Color, "background", "$00000000")
		output.setDefault(Color, "border-color", "$000000")
		output.setDefault(Number, "border-width", 0)
		output.setDefault(String, "border-style", "Solid")
		return output

	def generateAnonymousGroup(self, macros=None):
		return GroupNode(anonymous=True)

	def generateWidget(self, original, macros=None):
		if macros is None:
			macros = {}
		output = GroupNode(node=original)
		output.updateProperties(macros)
		return output

	def generateText(self, node, macros=None):
		if macros is None:
			macros = {}
		output = GroupNode(node=node)
		output.updateProperties(macros)
		return output


# ========================
#  Node Tests
# ========================

class TestNode(unittest.TestCase):
	def test_basic_construction(self):
		n = Node("Widget")
		self.assertEqual(n.classname, "Widget")
		self.assertIsNone(n.name)

	def test_construction_with_name(self):
		n = Node("Widget", name="w1")
		self.assertEqual(n.name, "w1")

	def test_default_geometry(self):
		n = Node("Widget")
		geom = n["geometry"].val()
		self.assertEqual(geom["x"], 0)
		self.assertEqual(geom["y"], 0)
		self.assertEqual(geom["width"], 0)
		self.assertEqual(geom["height"], 0)

	def test_construction_with_layout(self):
		n = Node("Widget", layout={"text": "hello"})
		self.assertIn("text", n)
		self.assertEqual(str(n["text"]), "hello")

	def test_copy_construction(self):
		original = Node("Widget", name="orig", layout={"text": "hello"})
		copied = Node("Widget", node=original)
		self.assertEqual(copied.name, "orig")
		self.assertEqual(str(copied["text"]), "hello")

	def test_set_default_new_key(self):
		n = Node("Widget")
		n.setDefault(Number, "padding", 5)
		self.assertEqual(int(n["padding"]), 5)

	def test_set_default_existing_key(self):
		n = Node("Widget", layout={"padding": 10})
		n.setDefault(Number, "padding", 5)
		# Existing value should be used, not default
		self.assertEqual(int(n["padding"]), 10)

	def test_make_internal(self):
		n = Node("Widget")
		n.makeInternal(Number, "hidden", 42)
		# Not in attrs
		self.assertNotIn("hidden", n)
		# But accessible via getProperty with internal=True
		val = n.getProperty("hidden", internal=True)
		self.assertEqual(int(val), 42)

	def test_set_property_bool(self):
		n = Node("Widget")
		n.setProperty("flag", True)
		self.assertIsInstance(n["flag"], Bool)

	def test_set_property_int(self):
		n = Node("Widget")
		n.setProperty("count", 5)
		self.assertIsInstance(n["count"], Number)

	def test_set_property_float(self):
		n = Node("Widget")
		n.setProperty("ratio", 1.5)
		self.assertIsInstance(n["ratio"], Double)

	def test_set_property_str(self):
		n = Node("Widget")
		n.setProperty("label", "hello")
		self.assertIsInstance(n["label"], String)

	def test_set_property_datatype(self):
		n = Node("Widget")
		c = Color("$FF0000")
		n.setProperty("color", c)
		self.assertIsInstance(n["color"], Color)

	def test_contains_checks_attrs(self):
		n = Node("Widget", layout={"visible": "true"})
		self.assertIn("visible", n)
		# Internal props not in __contains__
		self.assertNotIn("render-order", n)

	def test_position(self):
		n = Node("Widget")
		n.position(x=10, y=20)
		self.assertEqual(n["geometry"]["x"], 10)
		self.assertEqual(n["geometry"]["y"], 20)

	def test_deepcopy(self):
		n = Node("Widget", name="orig", layout={"text": "hello"})
		c = copy.deepcopy(n)
		self.assertEqual(c.name, "orig")
		self.assertEqual(str(c["text"]), "hello")
		# Modifications to copy don't affect original
		c["text"] = String("modified")
		self.assertEqual(str(n["text"]), "hello")


# ========================
#  GroupNode Tests
# ========================

class TestGroupNode(unittest.TestCase):
	def test_default_construction(self):
		g = GroupNode()
		self.assertEqual(g.classname, "Group")
		self.assertEqual(len(g.children), 0)

	def test_construction_with_children_list(self):
		child1 = Node("Widget", layout={"text": "a"})
		child2 = Node("Widget", layout={"text": "b"})
		g = GroupNode(layout={"children": [child1, child2]})
		self.assertEqual(len(g.children), 2)

	def test_append_deep_copies(self):
		child = Node("Widget", layout={"text": "original"})
		g = GroupNode()
		g.append(child)
		child["text"] = String("modified")
		# Group's copy should be unaffected
		self.assertEqual(str(g.children[0]["text"]), "original")

	def test_append_keep_original(self):
		child = Node("Widget")
		g = GroupNode()
		g.append(child, keep_original=True)
		self.assertIs(g.children[0], child)

	def test_placed_order_auto_assigned(self):
		g = GroupNode()
		c1 = Node("Widget")
		c2 = Node("Widget")
		g.append(c1)
		g.append(c2)
		self.assertEqual(g.children[0].placed_order, 0)
		self.assertEqual(g.children[1].placed_order, 1)

	def test_iter_sorts_by_render_order(self):
		g = GroupNode()
		c1 = Node("Widget")
		c1.setProperty("render-order", 2, internal=True)
		c2 = Node("Widget")
		c2.setProperty("render-order", 0, internal=True)
		c3 = Node("Widget")
		c3.setProperty("render-order", 1, internal=True)
		g.append(c1)
		g.append(c2)
		g.append(c3)
		orders = [int(c["render-order"]) for c in g]
		self.assertEqual(orders, [0, 1, 2])

	def test_place_grows_geometry(self):
		g = GroupNode()
		g["geometry"] = Rect("0x0x0x0")
		child = Node("Widget")
		child["geometry"] = Rect("0x0x100x50")
		g.place(child)
		self.assertGreaterEqual(g["geometry"]["width"], 100)
		self.assertGreaterEqual(g["geometry"]["height"], 50)

	def test_place_does_not_shrink(self):
		g = GroupNode()
		g["geometry"] = Rect("0x0x200x200")
		child = Node("Widget")
		child["geometry"] = Rect("0x0x50x50")
		g.place(child)
		self.assertEqual(g["geometry"]["width"], 200)
		self.assertEqual(g["geometry"]["height"], 200)

	def test_place_with_margins(self):
		g = GroupNode()
		g["geometry"] = Rect("0x0x0x0")
		g["margins"] = Rect("10x10x10x10")
		child = Node("Widget")
		child["geometry"] = Rect("0x0x100x50")
		g.place(child)
		# Child should be offset by margins
		self.assertEqual(g.children[-1]["geometry"]["x"], 10)
		self.assertEqual(g.children[-1]["geometry"]["y"], 10)

	def test_place_none_child(self):
		g = GroupNode()
		g.place(None)
		self.assertEqual(len(g.children), 0)

	def test_update_macros(self):
		g = GroupNode()
		g["geometry"] = Rect("0x0x200x100")
		g["margins"] = Rect("0x0x0x0")
		g.setDefault(Number, "border-width", 0)
		macros = {}
		g.updateMacros(g, macros)
		self.assertEqual(macros["__parentwidth__"], 200)
		self.assertEqual(macros["__parentheight__"], 100)
		self.assertEqual(macros["__parentcenterx__"], 100)
		self.assertEqual(macros["__parentcentery__"], 50)

	def test_update_macros_with_border(self):
		g = GroupNode()
		g["geometry"] = Rect("0x0x200x100")
		g["margins"] = Rect("0x0x0x0")
		g["border-width"] = Number(5)
		macros = {}
		g.updateMacros(g, macros)
		self.assertEqual(macros["__parentwidth__"], 190)  # 200 - 2*5
		self.assertEqual(macros["__parentheight__"], 90)   # 100 - 2*5


# ========================
#  FlowNode Tests
# ========================

class TestFlowNode(unittest.TestCase):
	def test_vertical_position_next(self):
		f = FlowNode(flow="vertical", layout={"padding": 5})
		f["padding"].apply({})
		f.setProperty("last-pos", 0, internal=True)

		child = Node("Widget")
		child["geometry"] = Rect("0x0x100x30")
		f.positionNext(child)
		self.assertEqual(child["geometry"]["y"], 0)

		child2 = Node("Widget")
		child2["geometry"] = Rect("0x0x100x20")
		f.positionNext(child2)
		self.assertEqual(child2["geometry"]["y"], 35)  # 30 + 5

	def test_horizontal_position_next(self):
		f = FlowNode(flow="horizontal", layout={"padding": 10})
		f["padding"].apply({})
		f.setProperty("last-pos", 0, internal=True)

		child = Node("Widget")
		child["geometry"] = Rect("0x0x50x30")
		f.positionNext(child)
		self.assertEqual(child["geometry"]["x"], 0)

		child2 = Node("Widget")
		child2["geometry"] = Rect("0x0x40x30")
		f.positionNext(child2)
		self.assertEqual(child2["geometry"]["x"], 60)  # 50 + 10

	def test_init_apply_resets(self):
		f = FlowNode(flow="vertical", layout={"padding": 5})
		f.setProperty("last-pos", 999, internal=True)
		f.initApply({})
		self.assertEqual(int(f.getProperty("last-pos", internal=True)), 0)


# ========================
#  LayoutNode Tests
# ========================

class TestLayoutNode(unittest.TestCase):
	def _make_layout(self, repeat_over="NUM", variable="N", start_at=0, increment=1, reverse=False):
		"""Create a LayoutNode with standard internal properties."""
		l = LayoutNode(layout={"repeat-over": repeat_over, "children": [SpacerNode(layout={"geometry": "10x10"})]})
		# Override defaults set by __init__
		l.setProperty("variable", variable, internal=True)
		l.setProperty("start-at", start_at, internal=True)
		l.setProperty("increment", increment, internal=True)
		l.setProperty("reverse", reverse, internal=True)
		return l

	def test_numeric_iteration(self):
		l = self._make_layout(repeat_over="NUM")
		l.initApply({"NUM": 3})
		items = list(l)
		self.assertEqual(len(items), 3)

	def test_list_iteration(self):
		l = self._make_layout(repeat_over="ITEMS")
		l.initApply({"ITEMS": ["a", "b", "c"]})
		items = list(l)
		self.assertEqual(len(items), 3)

	def test_dict_iteration(self):
		l = self._make_layout(repeat_over="MAP")
		l.initApply({"MAP": {"k1": "v1", "k2": "v2"}})
		items = list(l)
		self.assertEqual(len(items), 2)

	def test_unresolvable_repeat_over(self):
		l = self._make_layout(repeat_over="MISSING")
		l.initApply({})
		with self.assertRaises(Exception):
			list(l)

	def test_start_at_offset(self):
		l = self._make_layout(repeat_over="NUM", start_at=5)
		l.initApply({"NUM": 3})
		items = list(l)
		self.assertEqual(len(items), 3)

	def test_reverse_iteration(self):
		l = self._make_layout(repeat_over="ITEMS", reverse=True)
		l.initApply({"ITEMS": ["a", "b", "c"]})
		items = list(l)
		self.assertEqual(len(items), 3)


# ========================
#  CenterNode Tests
# ========================

class TestCenterNode(unittest.TestCase):
	def _run_centering(self, flow, child_geom, parent_center_x, parent_center_y):
		"""Helper to run the centering coroutine and return the repositioned node."""
		child = TextNode(layout={"geometry": child_geom, "text": "test"})
		center = CenterNode(flow=flow, subnode=child)

		gen = MockGenerator()
		applier = center.apply(gen)
		next(applier)
		applied = applier.send({})

		# Second phase: send updated parent macros
		try:
			next(applier)
			applier.send({
				"__parentcenterx__": parent_center_x,
				"__parentcentery__": parent_center_y,
			})
		except StopIteration:
			pass

		return applied

	def test_horizontal_centering(self):
		applied = self._run_centering("horizontal", "0x0x60x20", 150, 50)
		self.assertEqual(applied["geometry"]["x"], 120)  # 150 - 30

	def test_vertical_centering(self):
		applied = self._run_centering("vertical", "0x0x60x40", 150, 100)
		self.assertEqual(applied["geometry"]["y"], 80)  # 100 - 20

	def test_all_centering(self):
		applied = self._run_centering("all", "0x0x60x40", 150, 100)
		self.assertEqual(applied["geometry"]["x"], 120)  # 150 - 30
		self.assertEqual(applied["geometry"]["y"], 80)   # 100 - 20

	def test_oversized_child_negative_position(self):
		applied = self._run_centering("horizontal", "0x0x200x20", 50, 50)
		self.assertEqual(applied["geometry"]["x"], -50)  # 50 - 100


# ========================
#  ConditionalNode Tests
# ========================

class TestConditionalNode(unittest.TestCase):
	def _make_conditional(self, condition, children=None):
		if children is None:
			children = [TextNode(layout={"geometry": "100x20", "text": "child"})]
		c = ConditionalNode(layout={
			"condition": condition,
			"children": children,
		})
		return c

	def test_truthy_condition(self):
		c = self._make_conditional("SHOW")
		gen = MockGenerator()
		applier = c.apply(gen)
		next(applier)
		result = applier.send({"SHOW": "1"})
		self.assertIsNotNone(result)

	def test_falsy_condition(self):
		c = self._make_conditional("SHOW")
		gen = MockGenerator()
		applier = c.apply(gen)
		next(applier)
		# When condition is falsy, the coroutine ends with StopIteration
		with self.assertRaises(StopIteration):
			applier.send({"SHOW": "0"})

	def test_not_condition_inverts(self):
		c = ConditionalNode(layout={
			"condition": Not("SHOW"),
			"children": [TextNode(layout={"geometry": "100x20", "text": "child"})],
		})
		gen = MockGenerator()
		applier = c.apply(gen)
		next(applier)
		# Not(truthy) = falsy, so StopIteration
		with self.assertRaises(StopIteration):
			applier.send({"SHOW": "1"})


# ========================
#  ApplyNode Tests
# ========================

class TestWrapDatatype(unittest.TestCase):
	def test_wrap_bool(self):
		self.assertIsInstance(_wrap_datatype(True), Bool)
		self.assertIsInstance(_wrap_datatype(False), Bool)

	def test_wrap_int(self):
		self.assertIsInstance(_wrap_datatype(42), Number)

	def test_wrap_float(self):
		self.assertIsInstance(_wrap_datatype(3.14), Double)

	def test_wrap_str(self):
		self.assertIsInstance(_wrap_datatype("hello"), String)

	def test_wrap_datatype_passthrough(self):
		n = Number(5)
		self.assertIs(_wrap_datatype(n), n)

	def test_wrap_none(self):
		self.assertIsNone(_wrap_datatype(None))

	def test_wrap_list(self):
		result = _wrap_datatype([1, 2])
		self.assertIsInstance(result, list)

	def test_wrap_dict(self):
		result = _wrap_datatype({"a": 1})
		self.assertIsInstance(result, dict)

	def test_bool_before_int(self):
		# True is isinstance(int) but should be wrapped as Bool
		self.assertIsInstance(_wrap_datatype(True), Bool)
		self.assertNotIsInstance(_wrap_datatype(True), Number)


class TestApplyNode(unittest.TestCase):
	def test_basic_construction(self):
		a = ApplyNode(template="test")
		self.assertEqual(a.template, "test")
		self.assertEqual(a.classname, "Apply")

	def test_update_macros_explicit_override(self):
		a = ApplyNode(
			defaults={"A": "default_val"},
			macros={"A": "explicit_val"},
		)
		a.initApply({})

		output = GroupNode()
		output["geometry"] = Rect("0x0x100x100")
		output["margins"] = Rect("0x0x0x0")
		output.setDefault(Number, "border-width", 0)

		macros = {}
		a.updateMacros(output, macros)
		# Explicit macros should win over defaults
		self.assertEqual(str(macros["A"]), "explicit_val")

	def test_update_macros_default_used(self):
		a = ApplyNode(
			defaults={"B": "fallback"},
			macros={},
		)
		a.initApply({})

		output = GroupNode()
		output["geometry"] = Rect("0x0x100x100")
		output["margins"] = Rect("0x0x0x0")
		output.setDefault(Number, "border-width", 0)

		macros = {}
		a.updateMacros(output, macros)
		self.assertEqual(str(macros["B"]), "fallback")

	def test_update_macros_data_used(self):
		a = ApplyNode(
			defaults={},
			macros={},
		)
		a.initApply({"C": "from_data"})

		output = GroupNode()
		output["geometry"] = Rect("0x0x100x100")
		output["margins"] = Rect("0x0x0x0")
		output.setDefault(Number, "border-width", 0)

		macros = {}
		a.updateMacros(output, macros)
		self.assertEqual(str(macros["C"]), "from_data")

	def test_update_macros_resolution(self):
		a = ApplyNode(
			defaults={},
			macros={"PV": "{PREFIX}:value"},
		)
		a.initApply({"PREFIX": "IOC1"})

		output = GroupNode()
		output["geometry"] = Rect("0x0x100x100")
		output["margins"] = Rect("0x0x0x0")
		output.setDefault(Number, "border-width", 0)

		macros = {}
		a.updateMacros(output, macros)
		self.assertEqual(str(macros["PV"]), "IOC1:value")


if __name__ == "__main__":
	unittest.main()
