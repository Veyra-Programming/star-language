#!/usr/bin/env python3
"""
Star Language Comprehensive Test Suite Runner
Runs all unit and conformance tests.
"""

import unittest
import sys
import os

# Configure UTF-8 encoding on standard streams to avoid Windows charmap issues
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Set working directory to project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT_DIR)
sys.path.insert(0, ROOT_DIR)

def main():
    print("=" * 60)
    print("🌟 Running Star Language Test Suite")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py", top_level_dir=ROOT_DIR)




    runner = unittest.TextTestRunner(verbosity=2)


    result = runner.run(suite)


    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print(f"✅ ALL {result.testsRun} TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        return 0
    else:
        print(f"❌ {len(result.failures)} FAILURE(S), {len(result.errors)} ERROR(S)")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
