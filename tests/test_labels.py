import ast
import unittest
from pathlib import Path

from src.service import LabelService
from src.sqlite_adapter import SqliteLabelStore


class LabelBehavior(unittest.TestCase):
    def setUp(self):
        self.store = SqliteLabelStore()
        self.addCleanup(self.store.db.close)
        self.service = LabelService(self.store)

    def replace(self, original, replacement):
        if not hasattr(self.service, "set_labels"):
            self.skipTest("Label replacement is introduced by the feature branches")
        self.store.replace_labels("one", original)
        self.store.replace_labels("other", ["untouched"])
        self.service.set_labels("one", replacement)
        self.assertEqual(self.service.labels_for("one"), replacement)
        self.assertEqual(self.service.labels_for("other"), ["untouched"])

    def test_create(self):
        self.replace([], ["blue", "red"])

    def test_clear(self):
        self.replace(["old"], [])

    def test_reorder(self):
        self.replace(["x", "y"], ["y", "x"])

    def test_repeated_labels(self):
        self.replace(["x"], ["a", "a"])

    def test_replace(self):
        self.replace(["a", "b"], ["new"])

    def test_service_imports_only_the_port(self):
        source = Path(__file__).resolve().parents[1] / "src/service.py"
        tree = ast.parse(source.read_text())
        self.assertEqual([n.module for n in ast.walk(tree)
                          if isinstance(n, ast.ImportFrom)], ["src.ports"])
        self.assertFalse(any(isinstance(n, ast.Import) for n in ast.walk(tree)))
