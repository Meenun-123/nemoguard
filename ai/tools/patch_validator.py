import ast
from typing import Dict, Any

class PatchValidator:
    """Validates unified diff syntax and ensures patched code compiles cleanly."""

    def validate_code_compilation(self, code: str) -> Dict[str, Any]:
        """Verify that Python code parses without syntax errors."""
        try:
            ast.parse(code)
            return {
                "valid": True,
                "error": None
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"SyntaxError at line {e.lineno}, column {e.offset}: {e.msg}"
            }

    def validate_diff_format(self, diff: str) -> Dict[str, Any]:
        """Validate unified diff formatting."""
        lines = diff.strip().splitlines()
        has_orig = any(l.startswith("--- ") for l in lines)
        has_new = any(l.startswith("+++ ") for l in lines)
        has_hunk = any(l.startswith("@@ ") for l in lines)

        is_valid = has_orig and has_new and has_hunk
        return {
            "valid": is_valid,
            "has_header": has_orig and has_new,
            "has_hunk": has_hunk,
            "line_count": len(lines)
        }
