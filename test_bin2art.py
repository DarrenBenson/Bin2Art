#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import shutil
from typing import List, Optional

class Bin2ArtTester:
    """Test suite for bin2art.py"""
    
    def __init__.py


    def __init__(self) -> None:
        """Initialize test environment and tracking."""
        self.test_dir = Path("test_output")
        self.test_file = "test.rom"
        self.bin2art = "bin2art.py"
        self.generated_files: List[Path] = []
    
    def test_basic_conversion(self) -> None:
        """
        Test basic binary to image conversion with default settings.
        Verifies that a basic conversion works without any special parameters.
        """
        print("\n🔍 Testing basic conversion...")
        
        # Setup
        print("  Setting up test file...")
        self._create_test_file()
        expected_output = f"{self.test_file.replace('.rom', '.png')}"
        
        # Execute
        print("  Running basic conversion...")
        result = self._run_bin2art()
        
        # Assert
        if result.returncode == 0 and Path(expected_output).exists():
            print("  ✅ Basic conversion successful")
            print(f"  📁 Output file created: {expected_output}")
        else:
            print("  ❌ Basic conversion failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")

    def test_color_modes(self) -> None:
        """
        Test all available color modes.
        Ensures each color mode produces a valid output file.
        """
        print("\n🎨 Testing color modes...")
        color_modes = ['normal', 'complement', 'amplified', 'grayscale', 
                      'sepia', 'neon', 'pastel']
        
        for color_mode in color_modes:
            print(f"\n  Testing {color_mode} color mode...")
            
            # Execute
            result = self._run_bin2art(f"--color {color_mode}")
            output_file = Path(f"{self.test_file.replace('.rom', '.png')}")
            
            # Assert
            if result.returncode == 0 and output_file.exists():
                print(f"  ✅ {color_mode.capitalize()} mode successful")
                print(f"  📁 Output file: {output_file}")
            else:
                print(f"  ❌ {color_mode.capitalize()} mode failed")
                if result.stderr:
                    print(f"  Error: {result.stderr}")

    def test_effect_styles(self) -> None:
        """
        Test all available effect styles.
        Verifies that each effect produces a unique output file.
        """
        print("\n✨ Testing effect styles...")
        effects = ['none', 'mirror', 'rotate', 'kaleidoscope', 
                  'spiral', 'waves', 'mosaic', 'fractal']
        
        for effect in effects:
            print(f"\n  Testing {effect} effect...")
            
            # Execute
            result = self._run_bin2art(f"--effect {effect}")
            output_file = Path(f"{self.test_file.replace('.rom', '.png')}")
            
            # Assert
            if result.returncode == 0 and output_file.exists():
                print(f"  ✅ {effect.capitalize()} effect successful")
                print(f"  📁 Output file: {output_file}")
            else:
                print(f"  ❌ {effect.capitalize()} effect failed")
                if result.stderr:
                    print(f"  Error: {result.stderr}")

    def test_posterize(self) -> None:
        """
        Test posterize effect.
        Ensures the posterize effect properly reduces colors in the output.
        """
        print("\n🎯 Testing posterize effect...")
        
        # Setup
        print("  Setting up test file...")
        self._create_test_file()
        
        # Execute
        print("  Applying posterize effect...")
        result = self._run_bin2art("--posterize")
        output_file = Path(f"{self.test_file.replace('.rom', '.png')}")
        
        # Assert
        if result.returncode == 0 and output_file.exists():
            print("  ✅ Posterize effect successful")
            print(f"  📁 Output file: {output_file}")
        else:
            print("  ❌ Posterize effect failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")

    def _run_bin2art(self, args: str = "") -> subprocess.CompletedProcess:
        """
        Run bin2art with specified arguments.

        Args:
            args: Command line arguments to pass

        Returns:
            CompletedProcess instance with execution results
        """
        cmd = f"python {self.bin2art} {args}"
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)

    def _create_test_file(self) -> None:
        """
        Create a test binary file with random data.
        Used for testing image generation.
        """
        with open(self.test_file, 'wb') as f:
            f.write(os.urandom(1024))
        self.generated_files.append(Path(self.test_file))

    def cleanup(self) -> None:
        """
        Clean up all test artifacts.
        Removes generated files, test files, and test directory.
        """
        print("\nCleaning up test environment...")
        
        # Clean up generated images
        for file in Path().glob("*.png"):
            if file.exists():  # Check if file exists before trying to remove
                try:
                    file.unlink()
                    print(f"Removed generated image: {file}")
                except Exception as e:
                    print(f"Warning: Could not remove {file}: {e}")
        
        # Clean up test files
        for file in self.generated_files:
            if file.exists():  # Check if file exists before trying to remove
                try:
                    file.unlink()
                    print(f"Removed test file: {file}")
                except Exception as e:
                    print(f"Warning: Could not remove {file}: {e}")
        
        # Clean up test directory
        if self.test_dir.exists():
            try:
                shutil.rmtree(self.test_dir)
                print(f"Removed test directory: {self.test_dir}")
            except Exception as e:
                print(f"Warning: Could not remove {self.test_dir}: {e}")
        
        print("Cleanup complete")

def main() -> None:
    """
    Main test execution function.
    Runs all tests and ensures cleanup occurs.
    """
    print("\n=== 🧪 Starting Bin2Art Test Suite ===")
    
    tester = Bin2ArtTester()
    total_tests = 4
    passed_tests = 0
    
    try:
        # Run all tests
        test_functions = [
            tester.test_basic_conversion,
            tester.test_color_modes,
            tester.test_effect_styles,
            tester.test_posterize
        ]
        
        for test_func in test_functions:
            try:
                test_func()
                passed_tests += 1
            except AssertionError as e:
                print(f"❌ Test failed: {test_func.__name__}")
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"❌ Test error: {test_func.__name__}")
                print(f"Error: {str(e)}")
        
        print("\n=== 📊 Test Summary ===")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        
        if passed_tests == total_tests:
            print("\n✨ All tests passed successfully! ✨")
        else:
            print("\n⚠️ Some tests failed. Check output above for details.")
            
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main() 