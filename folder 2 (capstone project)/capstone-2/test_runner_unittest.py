"""
Standalone Unittest Test Suite Runner.
Executes test classes via standard Python unittest discovery and runner.
"""

import unittest
import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tests.test_login import TestLogin
from tests.test_search import TestSearch

def build_test_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # Load test cases from both test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLogin))
    suite.addTests(loader.loadTestsFromTestCase(TestSearch))

    return suite

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  RUNNING SELENIUM TEST SUITE VIA UNITTEST RUNNER")
    print("=" * 70 + "\n")

    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = build_test_suite()
    result = runner.run(test_suite)

    print("\n" + "=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70 + "\n")

    sys.exit(0 if result.wasSuccessful() else 1)