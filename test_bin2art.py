#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import shutil

class Bin2ArtTester:
    """Test suite for bin2art.py"""
    
    def __init__(self):
        self.test_dir = Path("test_output")
        self.test_file = "test.rom"
        self.bin2art = "bin2art.py"
        
        # Create test binary file if it doesn't exist
        if not os.path.exists(self.test_file):
            self._create_test_file()
    
    def setup(self):
        """Prepare test environment"""
        print("\nSetting up test environment...")
        # Create test output directory
        self.test_dir.mkdir(exist_ok=True)
        print(f"Created test directory: {self.test_dir}")
    
    def cleanup(self):
        """Clean up test files"""
        print("\nCleaning up test environment...")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        print("Cleanup complete")
    
    def _create_test_file(self):
        """Create a test binary file"""
        print("Creating test binary file...")
        # Create 1KB of random data
        with open(self.test_file, 'wb') as f:
            f.write(os.urandom(1024))
    
    def run_test(self, args=""):
        """Run bin2art with specified arguments"""
        cmd = f"python {self.bin2art} {args}"
        print(f"\nTesting: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Test passed")
                return True
            else:
                print("❌ Test failed")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            return False
    
    def test_all(self):
        """Run all tests"""
        tests = [
            # Basic functionality
            "",  # Default settings
            
            # Color modes
            "--color normal",
            "--color complement",
            "--color amplified",
            "--color grayscale",
            "--color sepia",
            "--color neon",
            "--color pastel",
            
            # Effects
            "--effect none",
            "--effect mirror",
            "--effect rotate",
            "--effect kaleidoscope",
            "--effect spiral",
            "--effect waves",
            "--effect mosaic",
            "--effect fractal",
            
            # Post-processing
            "--blur",
            "--enhance-color",
            "--enhance-contrast",
            "--posterize",
            "--all-effects",
            
            # Combinations
            "--color neon --effect spiral",
            "--color sepia --effect mirror --posterize",
            "--effect kaleidoscope --blur --enhance-color",
            
            # Edge cases
            "--color normal --effect none --posterize",
            "--color amplified --effect mirror --all-effects",
        ]
        
        total = len(tests)
        passed = 0
        failed = []
        
        print("\n=== Starting Bin2Art Test Suite ===")
        print(f"Total tests to run: {total}")
        
        for test in tests:
            if self.run_test(test):
                passed += 1
            else:
                failed.append(test)
        
        print("\n=== Test Summary ===")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {len(failed)}")
        
        if failed:
            print("\nFailed tests:")
            for test in failed:
                print(f"- {test}")

def main():
    tester = Bin2ArtTester()
    try:
        tester.setup()
        tester.test_all()
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main() 