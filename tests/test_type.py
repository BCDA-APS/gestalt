import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gestalt.Type import (
	json_like, PartialSubFormatter, PartialSubDict,
	DataType, String, Number, Double, Bool, Not, Enum, Set
)


class TestJsonLike(unittest.TestCase):
	def test_non_string_int(self):
		self.assertFalse(json_like(42))

	def test_non_string_none(self):
		self.assertFalse(json_like(None))

	def test_non_string_list(self):
		self.assertFalse(json_like([1, 2]))

	def test_non_string_dict(self):
		self.assertFalse(json_like({"a": 1}))

	def test_non_string_bool(self):
		self.assertFalse(json_like(True))

	def test_dict_like(self):
		self.assertTrue(json_like("{key: value}"))

	def test_no_colon_in_braces(self):
		# This is a macro placeholder, not a dict
		self.assertFalse(json_like("{MY_MACRO}"))

	def test_list_like(self):
		self.assertTrue(json_like("[1, 2, 3]"))

	def test_empty_list(self):
		self.assertTrue(json_like("[]"))

	def test_empty_string(self):
		self.assertFalse(json_like(""))

	def test_plain_string(self):
		self.assertFalse(json_like("hello world"))

	def test_unterminated_brace(self):
		self.assertFalse(json_like("{key: val"))

	def test_unterminated_bracket(self):
		self.assertFalse(json_like("[1, 2"))

	def test_braces_no_colon(self):
		self.assertFalse(json_like("{ }"))

	def test_braces_with_colon(self):
		self.assertTrue(json_like("{:}"))

	def test_nested_structure(self):
		self.assertTrue(json_like("{a: [1, 2]}"))


class TestPartialSubFormatter(unittest.TestCase):
	def test_empty_format_spec(self):
		f = PartialSubFormatter("X")
		self.assertEqual(format(f, ""), "{X}")

	def test_with_format_spec(self):
		f = PartialSubFormatter("X")
		self.assertEqual(format(f, "d"), "{X:d}")

	def test_complex_format_spec(self):
		f = PartialSubFormatter("val")
		self.assertEqual(format(f, ">10s"), "{val:>10s}")


class TestPartialSubDict(unittest.TestCase):
	def test_known_key(self):
		d = PartialSubDict({"A": "hello"})
		self.assertEqual(d["A"], "hello")

	def test_unknown_key(self):
		d = PartialSubDict({})
		result = d["X"]
		self.assertIsInstance(result, PartialSubFormatter)

	def test_partial_substitution(self):
		result = "{A}_{B}".format_map(PartialSubDict({"A": "hello"}))
		self.assertEqual(result, "hello_{B}")

	def test_full_substitution(self):
		result = "{A}_{B}".format_map(PartialSubDict({"A": "hello", "B": "world"}))
		self.assertEqual(result, "hello_world")

	def test_no_substitution(self):
		result = "{A}_{B}".format_map(PartialSubDict({}))
		self.assertEqual(result, "{A}_{B}")

	def test_format_spec_preserved(self):
		result = "{X:02d}".format_map(PartialSubDict({}))
		self.assertEqual(result, "{X:02d}")

	def test_format_spec_applied(self):
		result = "{X:02d}".format_map(PartialSubDict({"X": 5}))
		self.assertEqual(result, "05")


class TestDataTypeConstructor(unittest.TestCase):
	def test_none_value(self):
		d = DataType("string", None)
		self.assertEqual(d.value, "")
		self.assertTrue(d.standard)

	def test_zero_int(self):
		d = DataType("number", 0)
		self.assertEqual(d.value, "0")
		self.assertTrue(d.standard)

	def test_empty_string(self):
		d = DataType("string", "")
		self.assertEqual(d.value, "")

	def test_plain_string(self):
		d = DataType("string", "hello")
		self.assertEqual(d.value, "hello")
		self.assertTrue(d.standard)

	def test_json_like_dict(self):
		d = DataType(None, "{a: 1, b: 2}")
		self.assertTrue(d.dict)
		self.assertFalse(d.standard)
		self.assertEqual(d.typ, "dict")

	def test_json_like_list(self):
		d = DataType(None, "[1, 2, 3]")
		self.assertTrue(d.list)
		self.assertFalse(d.standard)
		self.assertEqual(d.typ, "list")

	def test_empty_list_stays_string(self):
		# "[]" is json_like but yaml parses to [], len==0, so stays string
		d = DataType("string", "[]")
		self.assertTrue(d.standard)

	def test_null_list_stays_string(self):
		# "[null]" parses to [None], first element is falsy
		d = DataType("string", "[null]")
		self.assertTrue(d.standard)

	def test_single_key_none_dict_stays_string(self):
		# "{foo: }" parses to {"foo": None} -- guard rejects it
		d = DataType("string", "{foo: }")
		self.assertTrue(d.standard)

	def test_macro_placeholder_stays_string(self):
		# "{MY_MACRO}" has no colon, json_like is False
		d = DataType("string", "{MY_MACRO}")
		self.assertTrue(d.standard)
		self.assertEqual(d.value, "{MY_MACRO}")

	def test_dict_input(self):
		d = DataType(None, {"key": "val"})
		self.assertTrue(d.dict)
		self.assertEqual(d.value, {"key": "val"})

	def test_list_input(self):
		d = DataType(None, [1, 2, 3])
		self.assertTrue(d.list)
		self.assertEqual(d.value, [1, 2, 3])

	def test_tuple_converted_to_list(self):
		d = DataType(None, (1, 2))
		self.assertTrue(d.list)
		self.assertIsInstance(d.value, list)

	def test_float_stored_as_string(self):
		d = DataType("double", 3.14)
		self.assertEqual(d.value, "3.14")

	def test_datatype_input_copies(self):
		original = DataType("string", "hello")
		original.apply({"X": "1"})
		copy = DataType("string", original)
		self.assertEqual(copy.value, "hello")
		self.assertEqual(len(copy.macros), 1)

	def test_yaml_parse_error_stays_string(self):
		# Invalid YAML inside braces with colon
		d = DataType("string", "{a: [invalid")
		self.assertTrue(d.standard)


class TestDataTypeVal(unittest.TestCase):
	def test_no_braces_fast_path(self):
		d = DataType("string", "hello")
		self.assertEqual(d.val(), "hello")

	def test_unresolved_macro(self):
		d = DataType("string", "{X}")
		self.assertEqual(d.val(), "{X}")

	def test_single_macro(self):
		d = DataType("string", "{X}_test")
		d.apply({"X": "hello"})
		self.assertEqual(d.val(), "hello_test")

	def test_multiple_macros_single_layer(self):
		d = DataType("string", "{A}_{B}")
		d.apply({"A": "hello", "B": "world"})
		self.assertEqual(d.val(), "hello_world")

	def test_multiple_macro_layers(self):
		d = DataType("string", "{A}_{B}")
		d.apply({"A": "first"})
		d.apply({"B": "second"})
		self.assertEqual(d.val(), "first_second")

	def test_partial_substitution(self):
		d = DataType("string", "{A}_{B}")
		d.apply({"A": "hello"})
		self.assertEqual(d.val(), "hello_{B}")

	def test_macro_produces_list(self):
		d = DataType("string", "{items}")
		d.apply({"items": "[1, 2, 3]"})
		result = d.val()
		self.assertIsInstance(result, list)

	def test_macro_produces_dict(self):
		d = DataType("string", "{data}")
		d.apply({"data": "{a: 1, b: 2}"})
		result = d.val()
		self.assertIsInstance(result, dict)

	def test_early_break_no_braces(self):
		d = DataType("string", "{X}")
		d.apply({"X": "resolved"})
		d.apply({"Y": "unused"})
		d.apply({"Z": "also_unused"})
		self.assertEqual(d.val(), "resolved")

	def test_dict_branch_simple(self):
		d = DataType(None, {"key": "value"})
		result = d.val()
		self.assertEqual(result["key"], "value")

	def test_dict_branch_with_macros(self):
		d = DataType(None, {"key": "{name}"})
		d.apply({"name": "resolved"})
		result = d.val()
		self.assertEqual(result["key"], "resolved")

	def test_dict_branch_updates_override(self):
		d = DataType(None, {"key": "original"})
		d["key"] = "overridden"
		result = d.val()
		self.assertEqual(result["key"], "overridden")

	def test_list_branch_simple(self):
		d = DataType(None, ["a", "b", "c"])
		result = d.val()
		self.assertEqual(result, ["a", "b", "c"])

	def test_list_branch_with_macros(self):
		d = DataType(None, ["{X}", "{Y}"])
		d.apply({"X": "hello", "Y": "world"})
		result = d.val()
		self.assertEqual(result, ["hello", "world"])

	def test_list_branch_updates_override(self):
		d = DataType(None, ["a", "b"])
		d[0] = "overridden"
		result = d.val()
		self.assertEqual(result[0], "overridden")

	def test_format_spec_preserved_unresolved(self):
		d = DataType("string", "{X:02d}")
		self.assertEqual(d.val(), "{X:02d}")

	def test_format_spec_applied_resolved(self):
		d = DataType("string", "{X:02d}")
		d.apply({"X": 5})
		self.assertEqual(d.val(), "05")

	def test_json_like_guard_in_dict_branch(self):
		# String values in dicts that aren't json_like shouldn't be YAML-parsed
		# Strings with ": " (colon-space) are valid YAML key-value syntax but
		# should NOT be parsed when not wrapped in braces
		d = DataType(None, {"macros": "P=prefix:,DESC=Label: Description"})
		result = d.val()
		self.assertIsInstance(result["macros"], str)


class TestDataTypeApply(unittest.TestCase):
	def test_apply_stacks_layers(self):
		d = DataType("string", "{X}")
		d.apply({"X": "first"})
		d.apply({"X": "second"})
		# Later apply is processed first (reversed), so second wins
		self.assertEqual(d.val(), "second")

	def test_apply_mutation_safety(self):
		d = DataType("string", "{X}")
		macros = {"X": "hello"}
		d.apply(macros)
		macros["X"] = "mutated"
		# Original should be unaffected
		self.assertEqual(d.val(), "hello")

	def test_multiple_layers_different_keys(self):
		d = DataType("string", "{A}_{B}")
		d.apply({"A": "first"})
		d.apply({"B": "second"})
		self.assertEqual(d.val(), "first_second")


class TestDataTypeFlatten(unittest.TestCase):
	def test_flatten_returns_same_type(self):
		s = String("{X}")
		s.apply({"X": "hello"})
		f = s.flatten()
		self.assertIsInstance(f, String)

	def test_flatten_resolves_value(self):
		s = String("{X}_test")
		s.apply({"X": "hello"})
		f = s.flatten()
		self.assertEqual(f.val(), "hello_test")

	def test_flatten_no_macros(self):
		s = String("{X}")
		s.apply({"X": "hello"})
		f = s.flatten()
		self.assertEqual(len(f.macros), 0)

	def test_flatten_number(self):
		n = Number("{X}")
		n.apply({"X": "42"})
		f = n.flatten()
		self.assertIsInstance(f, Number)
		self.assertEqual(f.val(), 42)


class TestDataTypeBool(unittest.TestCase):
	def test_zero_is_false(self):
		self.assertFalse(bool(String("0")))

	def test_one_is_true(self):
		self.assertTrue(bool(String("1")))

	def test_two_is_true(self):
		self.assertTrue(bool(String("2")))

	def test_false_string(self):
		self.assertFalse(bool(String("false")))

	def test_False_string(self):
		self.assertFalse(bool(String("False")))

	def test_true_string(self):
		self.assertTrue(bool(String("true")))

	def test_TRUE_string(self):
		self.assertTrue(bool(String("TRUE")))

	def test_empty_is_false(self):
		self.assertFalse(bool(String("")))

	def test_random_string_is_true(self):
		self.assertTrue(bool(String("hello")))


class TestDataTypeCopy(unittest.TestCase):
	def test_copy_preserves_value(self):
		s = String("hello")
		c = s.copy()
		self.assertEqual(c.val(), "hello")

	def test_copy_preserves_macros(self):
		s = String("{X}")
		s.apply({"X": "val"})
		c = s.copy()
		self.assertEqual(c.val(), "val")

	def test_copy_mutation_isolation(self):
		s = String("{X}")
		s.apply({"X": "original"})
		c = s.copy()
		c.apply({"X": "modified"})
		self.assertEqual(s.val(), "original")
		self.assertEqual(c.val(), "modified")

	def test_copy_preserves_updates(self):
		s = String("hello")
		s.apply({"X": "1"})
		c = s.copy()
		self.assertEqual(c.val(), "hello")
		self.assertEqual(len(c.macros), 1)


class TestSimpleSubclasses(unittest.TestCase):
	def test_string_type_tag(self):
		s = String("hello")
		self.assertEqual(s.typ, "string")

	def test_number_val_returns_int(self):
		n = Number("42")
		self.assertEqual(n.val(), 42)
		self.assertIsInstance(n.val(), int)

	def test_number_from_int(self):
		n = Number(42)
		self.assertEqual(n.val(), 42)

	def test_number_format(self):
		n = Number("42")
		self.assertEqual(format(n, "05d"), "00042")

	def test_number_with_macros(self):
		n = Number("{X}")
		n.apply({"X": "99"})
		self.assertEqual(n.val(), 99)

	def test_double_val_returns_float(self):
		d = Double("3.14")
		self.assertAlmostEqual(d.val(), 3.14)
		self.assertIsInstance(d.val(), float)

	def test_double_from_int_string(self):
		d = Double("42")
		self.assertEqual(d.val(), 42.0)

	def test_bool_type_tag(self):
		b = Bool("true")
		self.assertEqual(b.typ, "bool")

	def test_enum_type_tag(self):
		e = Enum("Class::Value")
		self.assertEqual(e.typ, "enum")

	def test_set_type_tag(self):
		s = Set("A | B")
		self.assertEqual(s.typ, "set")

	def test_not_inherits_from_string(self):
		n = Not("some_pv")
		self.assertIsInstance(n, String)
		self.assertIsInstance(n, DataType)

	def test_not_val(self):
		n = Not("some_pv")
		self.assertEqual(n.val(), "some_pv")


class TestDataTypeIntStrFloat(unittest.TestCase):
	def test_int_conversion(self):
		s = String("42")
		self.assertEqual(int(s), 42)

	def test_str_conversion(self):
		s = String("hello")
		self.assertEqual(str(s), "hello")

	def test_float_conversion(self):
		s = String("3.14")
		self.assertAlmostEqual(float(s), 3.14)

	def test_getitem_string(self):
		s = String("hello")
		self.assertEqual(s[0], "h")

	def test_getitem_dict(self):
		d = DataType(None, {"a": "1"})
		self.assertEqual(d["a"], "1")


if __name__ == "__main__":
	unittest.main()
