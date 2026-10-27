#!/usr/bin/env python3
"""Automated test runner for NemoGuard supporting both pytest and unittest discovery."""
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    print("=" * 65)
    print("  NemoGuard Offline Test Suite (CPU / Deterministic Mock)")
    print("=" * 65)

    try:
        import pytest
        print("[*] Running with pytest...")
        exit_code = pytest.main(["-v", str(ROOT_DIR / "tests")])
        if exit_code != 0:
            sys.exit(exit_code)
    except ImportError:
        print("[*] pytest not installed, using Python standard library unittest...")
        loader = unittest.TestLoader()
        suite = loader.discover(
            start_dir=str(ROOT_DIR / "tests"),
            pattern="test_*.py",
            top_level_dir=str(ROOT_DIR)
        )
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        if not result.wasSuccessful() or result.testsRun == 0:
            sys.exit(1)

    print("\n[SUCCESS] All test cases executed and PASSED!")

if __name__ == "__main__":
    main()
