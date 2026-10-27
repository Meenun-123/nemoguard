import unittest
from ai.tools.security_scanner import SecurityScanner

class TestSecurityScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SecurityScanner()

    def test_security_scanner_detects_sql_injection(self):
        code = """
def fetch_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
"""
        result = self.scanner.scan(code)
        self.assertTrue(result["syntax_valid"])
        self.assertGreaterEqual(result["total_issues"], 1)
        self.assertTrue(any(f["id"] == "SEC-001" for f in result["findings"]))

    def test_security_scanner_detects_eval(self):
        code = """
def calc(expr):
    return eval(expr)
"""
        result = self.scanner.scan(code)
        self.assertGreaterEqual(result["total_issues"], 1)
        self.assertTrue(any(f["id"] == "SEC-002" for f in result["findings"]))

    def test_security_scanner_clean_code(self):
        code = """
def add(a: int, b: int) -> int:
    return a + b
"""
        result = self.scanner.scan(code)
        self.assertTrue(result["syntax_valid"])
        self.assertEqual(result["total_issues"], 0)
        self.assertEqual(result["status"], "CLEAN")

if __name__ == "__main__":
    unittest.main()
