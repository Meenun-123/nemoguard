import sys
import io
import time
from typing import Dict, Any

class SandboxedRunner:
    """Safe runner for executing verification test cases in memory."""

    def run_test(self, test_code: str, target_code: str = "") -> Dict[str, Any]:
        """
        Executes the provided test assertions in an isolated local dictionary scope.
        Captures stdout/stderr, measures execution time, and detects failures.
        """
        start = time.time()
        combined_code = f"{target_code}\n\n{test_code}"
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        local_scope: Dict[str, Any] = {}
        passed = False
        error_msg = None

        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Execute combined target code and test assertions
            exec(combined_code, {"__builtins__": __builtins__}, local_scope)
            passed = True
        except AssertionError as ae:
            passed = False
            error_msg = f"AssertionError: {str(ae) or 'Assertion failed'}"
        except Exception as e:
            passed = False
            error_msg = f"{type(e).__name__}: {str(e)}"
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        duration = round(time.time() - start, 4)
        return {
            "passed": passed,
            "duration_seconds": duration,
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue(),
            "error": error_msg
        }
