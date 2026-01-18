#!/usr/bin/env python3

import unittest
import sys
from pathlib import Path


def run_tests():
    """Discover and run all tests."""
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.append(str(project_root))

    # Discover tests
    loader = unittest.TestLoader()
    start_dir = project_root / "tests"
    suite = loader.discover(start_dir, pattern="test_*.py")

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
