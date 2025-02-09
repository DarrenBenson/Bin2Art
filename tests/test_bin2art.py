#!/usr/bin/env python3

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
import unittest
from PIL import Image
import tempfile

# Add parent directory to path to import bin2art
sys.path.append(str(Path(__file__).parent.parent))

from bin2art import FileHandler, ImageProcessor, Config, ColorMode, EffectStyle

class ColoredTestResult(unittest.TestResult):
    """Custom test result formatter with colored output."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tests_run = []
        self.start_time = None

    def startTest(self, test):
        self.start_time = time.time()
        test_name = test.shortDescription() or str(test)
        print(f"\n🔄 Running: {test_name}")
        super().startTest(test)

    def addSuccess(self, test):
        elapsed_time = time.time() - self.start_time
        print(f"✅ Passed! ({elapsed_time:.3f}s)")
        super().addSuccess(test)

    def addError(self, test, err):
        print(f"❌ Error: {err[1]}")
        super().addError(test, err)

    def addFailure(self, test, err):
        print(f"❌ Failed: {err[1]}")
        super().addFailure(test, err)

    def addSkip(self, test, reason):
        print(f"⏭️  Skipped: {reason}")
        super().addSkip(test, reason)

class ColoredTestRunner(unittest.TextTestRunner):
    """Custom test runner that uses ColoredTestResult."""
    
    def __init__(self, *args, **kwargs):
        kwargs['resultclass'] = ColoredTestResult
        super().__init__(*args, **kwargs)

    def run(self, test):
        print("\n🚀 Starting test suite...")
        result = super().run(test)
        print("\n📊 Test Summary:")
        print(f"  Total tests: {result.testsRun}")
        print(f"  Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"  Failed: {len(result.failures)}")
        print(f"  Errors: {len(result.errors)}")
        print(f"  Skipped: {len(result.skipped)}")
        return result

class TestBin2Art(unittest.TestCase):
    """Test suite for bin2art.py"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        cls.project_dir = Path(__file__).parent.parent
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.config = Config()
        cls.file_handler = FileHandler(cls.config)
        cls.image_processor = ImageProcessor(cls.config)
        
        print(f"\n📁 Test environment setup:")
        print(f"  - Project dir: {cls.project_dir}")
        print(f"  - Test dir: {cls.test_dir}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests."""
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
            print(f"\n🧹 Cleaned up test directory: {cls.test_dir}")

    def setUp(self):
        """Set up before each test."""
        # Create a small test binary file
        self.test_file = self.test_dir / "test.rom"
        with open(self.test_file, "wb") as f:
            f.write(bytes(range(256)))  # Write 256 bytes of test data

    def tearDown(self):
        """Clean up after each test."""
        if self.test_file.exists():
            self.test_file.unlink()

    def test_file_handler_load_file_data(self):
        """
        Test that binary data is correctly loaded from a file.
        Verifies that the file content matches the expected byte pattern
        and the correct number of bytes are read.
        """
        # Setup
        expected_length = 256
        expected_first_byte = 0
        expected_last_byte = 255

        # Execute
        data = self.file_handler.load_file_data(str(self.test_file))

        # Assert
        self.assertEqual(len(data), expected_length, "File data length should be 256 bytes")
        self.assertEqual(data[0], expected_first_byte, "First byte should be 0")
        self.assertEqual(data[255], expected_last_byte, "Last byte should be 255")

    def test_file_handler_get_output_filename(self):
        """
        Test that output filenames are generated correctly with proper paths
        and extensions based on the input arguments.
        """
        # Setup
        class Args:
            output_dir = "output"
            format = "PNG"
        args = Args()
        input_filename = "test.rom"
        expected_path = os.path.join("output", "test.png")

        # Execute
        output_name = self.file_handler.get_output_filename(input_filename, args)

        # Assert
        self.assertEqual(output_name, expected_path, "Output filename should match expected format")

    def test_image_processor_calculate_dimensions(self):
        """
        Test that image dimensions are calculated correctly for various input sizes.
        Verifies that the output dimensions create a square image that can fit all bytes.
        """
        # Setup
        test_cases = [
            (9, 2, "3x3 pixels (9 bytes)"),
            (27, 3, "9x9 pixels (27 bytes)"),
            (100, 6, "36x36 pixels (100 bytes)")
        ]

        for input_size, expected_dim, msg in test_cases:
            with self.subTest(input_size=input_size):
                # Execute
                result = self.image_processor.calculate_dimensions(input_size)

                # Assert
                self.assertEqual(result, expected_dim, msg)

    def test_image_processor_get_rgb_values_normal(self):
        """
        Test that RGB values are correctly extracted from binary data
        in normal color mode without any transformations.
        """
        # Setup
        test_data = bytes([100, 150, 200])
        expected_rgb = (100, 150, 200)

        # Execute
        rgb = self.image_processor.get_rgb_values(test_data, 0, ColorMode.NORMAL)

        # Assert
        self.assertEqual(rgb, expected_rgb, "RGB values should match input data")

    def test_image_processor_get_rgb_values_grayscale(self):
        """
        Test that RGB values are correctly converted to grayscale
        ensuring all color channels are equal.
        """
        # Setup
        test_data = bytes([100, 150, 200])

        # Execute
        rgb = self.image_processor.get_rgb_values(test_data, 0, ColorMode.GRAYSCALE)

        # Assert
        self.assertEqual(rgb[0], rgb[1], "Grayscale R and G channels should be equal")
        self.assertEqual(rgb[1], rgb[2], "Grayscale G and B channels should be equal")

    def test_image_processor_create_image(self):
        """
        Test that images are created with correct dimensions, mode,
        and pixel data from binary input.
        """
        # Setup
        test_data = bytes([255, 0, 0] * 4)  # 4 red pixels
        dimensions = 2
        expected_size = (2, 2)
        expected_mode = "RGBA"

        # Execute
        image = self.image_processor.create_image(
            test_data, 
            dimensions,
            EffectStyle.NONE,
            ColorMode.NORMAL
        )

        # Assert
        self.assertIsInstance(image, Image.Image, "Should return a PIL Image")
        self.assertEqual(image.size, expected_size, "Image dimensions should be 2x2")
        self.assertEqual(image.mode, expected_mode, "Image mode should be RGBA")

    def test_color_modes(self):
        """
        Test that different color modes correctly transform RGB values
        according to their specific algorithms.
        """
        # Setup
        test_data = bytes([100, 150, 200])
        expected_complement = (155, 105, 55)

        # Execute & Assert - Complement mode
        rgb_complement = self.image_processor.get_rgb_values(test_data, 0, ColorMode.COMPLEMENT)
        self.assertEqual(rgb_complement, expected_complement, 
                        "Complement colors should be 255 minus original values")

        # Execute & Assert - Neon mode
        rgb_neon = self.image_processor.get_rgb_values(test_data, 0, ColorMode.NEON)
        self.assertTrue(all(v <= 255 for v in rgb_neon), 
                       "Neon values should not exceed 255")

    def test_effect_styles(self):
        """
        Test that all effect styles produce valid images with correct
        dimensions and color modes, regardless of the effect applied.
        """
        # Setup
        test_data = bytes([255, 0, 0] * 16)  # 16 red pixels
        dimensions = 4
        expected_size = (4, 4)
        expected_mode = "RGBA"

        for effect in EffectStyle:
            with self.subTest(effect=effect.value):
                # Execute
                image = self.image_processor.create_image(
                    test_data,
                    dimensions,
                    effect,
                    ColorMode.NORMAL
                )

                # Assert
                self.assertEqual(image.size, expected_size,
                               f"Image size should be {dimensions}x{dimensions} for {effect.value}")
                self.assertEqual(image.mode, expected_mode,
                               f"Image mode should be RGBA for {effect.value}")

    def test_binary_file_processing(self):
        """
        Test that binary files are correctly processed into images.
        Verifies that files of different sizes and patterns are handled properly
        and produce images with expected characteristics.
        """
        # Setup
        test_cases = [
            {
                'name': 'simple_pattern',
                'data': bytes([255, 0, 0] * 16),  # Simple red pattern
                'size': 4,
                'expected_pixels': [(255, 0, 0, 255)]  # Check first pixel
            },
            {
                'name': 'gradient',
                'data': bytes(range(256)),  # Gradient pattern
                'size': 10,
                'expected_pixels': [(0, 1, 2, 255)]  # Check first RGB triple
            },
            {
                'name': 'empty',
                'data': bytes([0] * 48),  # All black
                'size': 4,
                'expected_pixels': [(0, 0, 0, 255)]
            }
        ]

        for test_case in test_cases:
            with self.subTest(case=test_case['name']):
                # Setup - Create test binary file
                test_file = self.test_dir / f"{test_case['name']}.rom"
                with open(test_file, "wb") as f:
                    f.write(test_case['data'])

                # Execute
                # Load the binary data
                file_data = self.file_handler.load_file_data(str(test_file))
                
                # Create the image
                image = self.image_processor.create_image(
                    file_data,
                    test_case['size'],
                    EffectStyle.NONE,
                    ColorMode.NORMAL
                )

                # Assert
                # Verify image was created
                self.assertIsInstance(image, Image.Image, 
                    f"Should create valid image for {test_case['name']}")
                
                # Verify image dimensions
                expected_size = (test_case['size'], test_case['size'])
                self.assertEqual(image.size, expected_size,
                    f"Image should be {expected_size[0]}x{expected_size[1]} for {test_case['name']}")
                
                # Verify image mode
                self.assertEqual(image.mode, "RGBA",
                    f"Image should be in RGBA mode for {test_case['name']}")
                
                # Verify pixel data
                for expected_pixel in test_case['expected_pixels']:
                    pixel = image.getpixel((0, 0))  # Check first pixel
                    self.assertEqual(pixel, expected_pixel,
                        f"First pixel should match expected value for {test_case['name']}")

    def test_binary_file_processing_with_effects(self):
        """
        Test that binary files are correctly processed with different effects and color modes.
        Verifies that the combination of effects and color modes produce valid images.
        """
        # Setup
        test_data = bytes([255, 128, 0] * 64)  # Orange pattern
        test_file = self.test_dir / "effect_test.rom"
        with open(test_file, "wb") as f:
            f.write(test_data)

        # Test combinations of effects and color modes
        effects = [EffectStyle.NONE, EffectStyle.MIRROR, EffectStyle.ROTATE]
        color_modes = [ColorMode.NORMAL, ColorMode.GRAYSCALE, ColorMode.NEON]

        for effect in effects:
            for color_mode in color_modes:
                with self.subTest(effect=effect.value, color_mode=color_mode.value):
                    # Execute
                    file_data = self.file_handler.load_file_data(str(test_file))
                    image = self.image_processor.create_image(
                        file_data,
                        8,  # 8x8 image
                        effect,
                        color_mode
                    )

                    # Assert
                    self.assertIsInstance(image, Image.Image,
                        f"Should create valid image for {effect.value} effect and {color_mode.value} mode")
                    self.assertEqual(image.size, (8, 8),
                        f"Image should be 8x8 for {effect.value} effect and {color_mode.value} mode")
                    self.assertEqual(image.mode, "RGBA",
                        f"Image should be in RGBA mode for {effect.value} effect and {color_mode.value} mode")

                    # Verify image is not empty (has some non-zero pixels)
                    has_data = False
                    for x in range(8):
                        for y in range(8):
                            if sum(image.getpixel((x, y))[:3]) > 0:
                                has_data = True
                                break
                        if has_data:
                            break
                    
                    self.assertTrue(has_data,
                        f"Image should contain non-zero pixels for {effect.value} effect and {color_mode.value} mode")

if __name__ == '__main__':
    unittest.main(testRunner=ColoredTestRunner(verbosity=2)) 