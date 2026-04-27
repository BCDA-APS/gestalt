import unittest
import tempfile
import os
import sys
from pathlib import Path
from lxml import etree

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gestalt import Stylesheet, Datasheet
from gestalt.convert.qt.QtGenerator import generateQtFile

GESTALT_ROOT = str(Path(__file__).resolve().parent.parent)
WIDGETS_DIR = str(Path(GESTALT_ROOT) / "widgets")
LAYOUTS_DIR = str(Path(GESTALT_ROOT) / "layouts")


class RegressionTestBase(unittest.TestCase):
	"""Base class for regression tests with shared helpers."""

	@classmethod
	def setUpClass(cls):
		cls.temp_dir = tempfile.mkdtemp(prefix="gestalt_test_")

	@classmethod
	def tearDownClass(cls):
		import shutil
		shutil.rmtree(cls.temp_dir, ignore_errors=True)

	def _write_layout(self, layout_str, filename="test_layout.yml"):
		"""Write a layout string to a temp file and return the path."""
		path = os.path.join(self.temp_dir, filename)
		with open(path, "w") as f:
			f.write(layout_str)
		return path

	def _generate_qt(self, layout_path, data=None, include_dirs=None):
		"""Parse layout, generate Qt output, return output path."""
		if include_dirs is None:
			include_dirs = [".", WIDGETS_DIR, os.path.dirname(layout_path)]

		styles = Stylesheet.parse(layout_path, include_dirs)

		if data is None:
			data = {}

		output_path = layout_path.replace(".yml", ".ui")
		generateQtFile(styles, data, outputfile=output_path)

		return output_path

	def _count_widgets(self, ui_path):
		"""Parse a .ui file and return dict of {classname: count}."""
		tree = etree.parse(ui_path)
		counts = {}
		for widget in tree.iter("widget"):
			cls = widget.get("class", "unknown")
			counts[cls] = counts.get(cls, 0) + 1
		return counts

	def _assert_generates(self, layout_str, data=None, filename="test.yml"):
		"""Assert that a layout generates successfully and return widget counts."""
		path = self._write_layout(layout_str, filename)
		output = self._generate_qt(path, data)
		self.assertTrue(os.path.exists(output), f"Output file not created: {output}")
		self.assertGreater(os.path.getsize(output), 0, "Output file is empty")
		return self._count_widgets(output)


class TestSmokeSimpleWidgets(RegressionTestBase):
	"""Smoke tests for simple widget generation."""

	def test_text_widget(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Label: !Text
    geometry: 100x20
    text: "Hello World"
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 1)

	def test_text_monitor(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Monitor: !TextMonitor
    geometry: 100x20
    pv: "TEST:PV"
""")
		self.assertGreaterEqual(counts.get("caLineEdit", 0), 1)

	def test_text_entry(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Entry: !TextEntry
    geometry: 100x20
    pv: "TEST:PV"
""")
		self.assertGreaterEqual(counts.get("caTextEntry", 0), 1)

	def test_message_button(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Button: !MessageButton
    geometry: 100x30
    text: "Click Me"
    pv: "TEST:PV"
    value: 1
""")
		self.assertGreaterEqual(counts.get("caMessageButton", 0), 1)

	def test_led(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Status: !LED
    geometry: 20x20
    pv: "TEST:PV"
""")
		self.assertGreaterEqual(counts.get("caLed", 0), 1)

	def test_menu(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

MyMenu: !Menu
    geometry: 100x20
    pv: "TEST:PV"
""")
		self.assertGreaterEqual(counts.get("caMenu", 0), 1)


class TestSmokeLayouts(RegressionTestBase):
	"""Smoke tests for layout containers."""

	def test_hflow(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Row: !HFlow
    padding: 5
    children:
        - !Text { geometry: 50x20, text: "A" }
        - !Text { geometry: 50x20, text: "B" }
        - !Text { geometry: 50x20, text: "C" }
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 3)

	def test_vflow(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Col: !VFlow
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "A" }
        - !Text { geometry: 100x20, text: "B" }
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 2)

	def test_group_with_border(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Box: !Group
    geometry: 200x100
    border-width: 2
    border-color: $000000
    background: $CCCCCC
    children:
        - !Text { geometry: 100x20, text: "Inside" }
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 1)

	def test_tabbed_group(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Tabs: !TabbedGroup
    geometry: 400x300
    children:
        Tab1: !Tab
            - !Text { geometry: 100x20, text: "Page 1" }
        Tab2: !Tab
            - !Text { geometry: 100x20, text: "Page 2" }
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 2)


class TestSmokeRepeat(RegressionTestBase):
	"""Smoke tests for repeat/iteration patterns."""

	def test_numeric_repeat(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Items: !VRepeat
    repeat-over: "COUNT"
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "Item {N}" }
""", data={"COUNT": 4})
		self.assertGreaterEqual(counts.get("caLabel", 0), 4)

	def test_list_repeat(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Items: !HRepeat
    repeat-over: "NAMES"
    variable: "name"
    padding: 10
    children:
        - !Text { geometry: 80x20, text: "{name}" }
""", data={"NAMES": ["Alice", "Bob", "Charlie"]})
		self.assertGreaterEqual(counts.get("caLabel", 0), 3)

	def test_inline_list_repeat(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Items: !HRepeat
    repeat-over: [ "A", "B", "C" ]
    variable: "ID"
    padding: 5
    children:
        - !Text { geometry: 50x20, text: "{ID}" }
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 3)

	def test_grid_repeat(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Grid: !Grid
    repeat-over: "NUM"
    padding: 5
    children:
        - !Text { geometry: 80x20, text: "Cell {N}" }
""", data={"NUM": 6})
		self.assertGreaterEqual(counts.get("caLabel", 0), 6)


class TestSmokeTemplateApply(RegressionTestBase):
	"""Smoke tests for template/apply patterns."""

	def test_basic_template_apply(self):
		counts = self._assert_generates("""
#include colors.yml

_MyWidget: !Template:MyWidget
    - !Defaults
        label: "Default"
    - !Text
        geometry: 100x20
        text: "{label}"

Form: !Form
    title: "Test"

W1: !Apply:MyWidget { label: "Custom Label" }
W2: !Apply:MyWidget {}
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 2)

	def test_nested_template_apply(self):
		counts = self._assert_generates("""
#include colors.yml

_Inner: !Template:Inner
    - !Defaults
        text: "inner"
    - !Text
        geometry: 80x20
        text: "{text}"

_Outer: !Template:Outer
    - !Defaults
        label: "outer"
    - !VFlow
        padding: 5
        children:
            - !Text { geometry: 100x20, text: "{label}" }
            - !Apply:Inner { text: "{label}_detail" }

Form: !Form
    title: "Test"

Content: !Apply:Outer { label: "Hello" }
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 2)

	def test_conditional_if(self):
		counts = self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Shown: !If:show
    - !Text { geometry: 100x20, text: "Visible" }
""", data={"show": True})
		self.assertGreaterEqual(counts.get("caLabel", 0), 1)


class TestSmokePositioners(RegressionTestBase):
	"""Smoke tests for stretch/center/anchor modifiers."""

	def test_hcenter(self):
		self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"
    geometry: 400x200

Content: !Group
    geometry: 400x200
    children:
        - !HCenter:Text
            geometry: 100x20
            text: "Centered"
""")

	def test_hstretch(self):
		self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"
    geometry: 400x200

Stretched: !HStretch:Text
    geometry: 0x0x0x20
    text: "Stretched"
""")

	def test_multi_prefix(self):
		self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"
    geometry: 400x200

Positioned: !HCenter:VFlow
    padding: 5
    children:
        - !Text { geometry: 100x20, text: "A" }
        - !Text { geometry: 100x20, text: "B" }
""")


class TestSmokeWidgetIncludes(RegressionTestBase):
	"""Smoke tests using repo widget includes."""

	def test_with_color_includes(self):
		counts = self._assert_generates("""
#include colors.yml
#include color-schemes.yml

Form: !Form
    title: "Test"

Label: !Text
    geometry: 100x20
    text: "Colored"
    foreground: *alarm_red
    background: *white
""")
		self.assertGreaterEqual(counts.get("caLabel", 0), 1)

	def test_with_screen_header(self):
		counts = self._assert_generates("""
#include colors.yml
#include color-schemes.yml
#include screen-header.yml

Form: !Form
    title: "Test"

Header: !Apply:ScreenHeader { title: "My Screen" }
""")
		# ScreenHeader produces at least a label
		self.assertGreaterEqual(counts.get("caLabel", 0), 1)

	def test_with_on_off(self):
		counts = self._assert_generates("""
#include colors.yml
#include color-schemes.yml
#include on-off.yml

Form: !Form
    title: "Test"

Toggle: !Apply:OnOffText
    geometry: 80x20
    on-label: "Open"
    off-label: "Closed"
    control-pv: "TEST:PV"
""")
		total = sum(counts.values())
		self.assertGreater(total, 0)


class TestSmokeCaseInsensitive(RegressionTestBase):
	"""Verify case-insensitive tag handling."""

	def test_lowercase_tags(self):
		self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Row: !hflow
    padding: 5
    children:
        - !text { geometry: 50x20, text: "lower" }
""")

	def test_uppercase_tags(self):
		self._assert_generates("""
#include colors.yml

Form: !Form
    title: "Test"

Row: !HFLOW
    padding: 5
    children:
        - !TEXT { geometry: 50x20, text: "upper" }
""")


class TestSmokeBuiltinLayouts(RegressionTestBase):
	"""Smoke tests using the built-in layouts from the repo."""

	def test_multimotor_layout(self):
		layout_path = str(Path(LAYOUTS_DIR) / "multimotor" / "layout.yml")
		if not os.path.exists(layout_path):
			self.skipTest("multimotor layout not found")

		include_dirs = [".", WIDGETS_DIR, str(Path(LAYOUTS_DIR) / "multimotor")]
		styles = Stylesheet.parse(layout_path, include_dirs)
		data = {"MOTORS": 4, "ASPECT": 2.0, "PADDING": 15}

		output_path = os.path.join(self.temp_dir, "multimotor.ui")
		generateQtFile(styles, data, outputfile=output_path)

		self.assertTrue(os.path.exists(output_path))
		self.assertGreater(os.path.getsize(output_path), 0)

		counts = self._count_widgets(output_path)
		total = sum(counts.values())
		self.assertGreater(total, 10, f"Expected many widgets, got {total}")

	def test_full_example_layout(self):
		layout_path = str(Path(LAYOUTS_DIR) / "fullExample" / "layout.yml")
		if not os.path.exists(layout_path):
			self.skipTest("fullExample layout not found")

		include_dirs = [".", WIDGETS_DIR, str(Path(LAYOUTS_DIR) / "fullExample")]
		styles = Stylesheet.parse(layout_path, include_dirs)
		data = {"Inputs": 10, "LEDs": 24, "Enable_Shapes": True, "Tank_Color": "$7FFFD4"}

		output_path = os.path.join(self.temp_dir, "fullExample.ui")
		generateQtFile(styles, data, outputfile=output_path)

		self.assertTrue(os.path.exists(output_path))
		self.assertGreater(os.path.getsize(output_path), 0)

		counts = self._count_widgets(output_path)
		total = sum(counts.values())
		self.assertGreater(total, 20, f"Expected many widgets, got {total}")


if __name__ == "__main__":
	unittest.main()
