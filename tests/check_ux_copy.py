#!/usr/bin/env python3
"""
CLI Copy Check Script (Rule 7)
Scans NGIS codebase for forbidden words, bare buttons, error messages without fixes, and badge color misuse.
Fails with exit code 1 if any violations exist, or passes with exit code 0.
"""

import sys
import unittest
from test_ux_copy import TestUXCopyAndComponentStates

def main():
    print("============================================================")
    print("NGIS ERP — UX Writing & Component State Rule Validator (Rules 1–12)")
    print("============================================================")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUXCopyAndComponentStates)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(f"\n[FAIL] Validation found {len(result.failures) + len(result.errors)} issues.")
        sys.exit(1)
    else:
        print(f"\n[PASS] All {result.testsRun} tests passed with 0 warnings.")
        sys.exit(0)

if __name__ == '__main__':
    main()

