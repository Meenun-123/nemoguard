import ast
import re
from typing import Dict, Any, List

class SecurityScanner:
    """Static AST and regex vulnerability scanner for Python source code."""

    COMMON_PATTERNS = [
        {
            "id": "SEC-001",
            "name": "SQL Injection (Unsanitized Dynamic Query)",
            "severity": "CRITICAL",
            "regex": r"(?:f[\"'].*(?:SELECT|INSERT|UPDATE|DELETE|\bFROM\b)|\.format\(.*(?:SELECT|INSERT|UPDATE|DELETE)|(?:execute|cursor\.execute)\s*\(\s*f?[\"'].*(?:SELECT|INSERT|UPDATE|DELETE))",
            "description": "SQL query constructed via f-string or string formatting allows arbitrary SQL injection."
        },
        {
            "id": "SEC-002",
            "name": "Unsafe Dynamic Code Execution (eval/exec)",
            "severity": "HIGH",
            "regex": r"\b(eval|exec)\s*\(",
            "description": "Direct execution of dynamic strings may allow remote code execution."
        },
        {
            "id": "SEC-003",
            "name": "Command Injection (subprocess/os.system)",
            "severity": "CRITICAL",
            "regex": r"(?:os\.system|subprocess\.Popen|subprocess\.run|subprocess\.check_output)\s*\(\s*f?[\"'].*shell\s*=\s*True",
            "description": "Executing shell commands with shell=True or unescaped user inputs invites shell injection."
        },
        {
            "id": "SEC-004",
            "name": "Hardcoded Secret / API Key",
            "severity": "HIGH",
            "regex": r"(?:api_key|secret|password|token)\s*=\s*[\"'][A-Za-z0-9_\-]{16,}[\"']",
            "description": "High entropy string or credential embedded directly in source code."
        }
    ]

    def scan(self, code: str) -> Dict[str, Any]:
        findings: List[Dict[str, Any]] = []

        # 1. Regex pattern matching
        lines = code.splitlines()
        for idx, line in enumerate(lines, start=1):
            for pat in self.COMMON_PATTERNS:
                if re.search(pat["regex"], line, re.IGNORECASE):
                    findings.append({
                        "id": pat["id"],
                        "name": pat["name"],
                        "severity": pat["severity"],
                        "line": idx,
                        "line_content": line.strip(),
                        "description": pat["description"]
                    })

        # 2. Python AST Syntax validation
        syntax_valid = True
        syntax_error = None
        try:
            tree = ast.parse(code)
            # AST Node visitor for deep checks
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                        if not any(f["id"] == "SEC-002" and f["line"] == node.lineno for f in findings):
                            findings.append({
                                "id": "SEC-002",
                                "name": "Unsafe Dynamic Code Execution (eval/exec)",
                                "severity": "HIGH",
                                "line": node.lineno,
                                "line_content": lines[node.lineno - 1].strip() if node.lineno <= len(lines) else "",
                                "description": "Call to eval/exec detected in AST traversal."
                            })
        except SyntaxError as se:
            syntax_valid = False
            syntax_error = f"Line {se.lineno}: {se.msg}"

        return {
            "syntax_valid": syntax_valid,
            "syntax_error": syntax_error,
            "total_issues": len(findings),
            "findings": findings,
            "status": "VULNERABILITIES_FOUND" if findings else "CLEAN"
        }
