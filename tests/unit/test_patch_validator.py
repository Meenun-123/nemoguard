import unittest
from ai.tools.patch_validator import PatchValidator

class TestPatchValidator(unittest.TestCase):
    def setUp(self):
        self.validator = PatchValidator()

    def test_patch_validator_compilation_valid(self):
        code = "def valid_func():\n    return 42\n"
        res = self.validator.validate_code_compilation(code)
        self.assertTrue(res["valid"])
        self.assertIsNone(res["error"])

    def test_patch_validator_compilation_syntax_error(self):
        code = "def broken_func(\n"
        res = self.validator.validate_code_compilation(code)
        self.assertFalse(res["valid"])
        self.assertIn("SyntaxError", res["error"])

    def test_patch_validator_diff_format(self):
        valid_diff = """--- target.py
+++ target.py
@@ -1,2 +1,2 @@
-bad_code()
+good_code()
"""
        res = self.validator.validate_diff_format(valid_diff)
        self.assertTrue(res["valid"])
        self.assertTrue(res["has_header"])
        self.assertTrue(res["has_hunk"])

if __name__ == "__main__":
    unittest.main()
