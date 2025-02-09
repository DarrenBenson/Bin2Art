# This program converts binary files (ROMs, disk images, audio files, etc.) into abstract art
# It does this by reading the binary data and converting each 3 bytes into RGB pixel values
# The resulting image is a visual representation of the file's binary structure

import os
import mmap
from numpy import ceil, sqrt
from PIL import Image, ImageFilter, ImageEnhance
from typing import List, Tuple
import math
import argparse
from enum import Enum
from dataclasses import dataclass

# Enums for different modes and styles
class ColorMode(Enum):
    NORMAL = 'normal'
    COMPLEMENT = 'complement'
    AMPLIFIED = 'amplified'
    GRAYSCALE = 'grayscale'
    SEPIA = 'sepia'
    NEON = 'neon'
    PASTEL = 'pastel'

class EffectStyle(Enum):
    NONE = 'none'
    MIRROR = 'mirror'
    ROTATE = 'rotate'
    KALEIDOSCOPE = 'kaleidoscope'
    SPIRAL = 'spiral'
    WAVES = 'waves'
    MOSAIC = 'mosaic'
    FRACTAL = 'fractal'

@dataclass
class Config:
    """Configuration settings for the art generator"""
    INCLUDED_EXTENSIONS: List[str] = ["dsk", "tap", "a26", "cdt", "rom", "mp3"]
    OUTPUT_IMAGE_SIZE: int = 1920
    BYTES_PER_PIXEL: int = 3
    DEFAULT_ALPHA: int = 255
    POSTER_COLORS: int = 8
    BLUR_RADIUS: float = 2.0
    COLOR_ENHANCE: float = 1.5
    CONTRAST_ENHANCE: float = 1.3

class FileHandler:
    """Handles all file-related operations"""
    
    @staticmethod
    def get_output_filename(input_filename: str, args: argparse.Namespace) -> str:
        base_filename = os.path.splitext(input_filename)[0]
        output_path = os.path.join(args.output_dir, f"{base_filename}.{args.format.lower()}")
        return output_path

    @staticmethod
    def load_file_data(filename: str) -> bytes:
        """Reads binary data using memory mapping for efficiency"""
        with open(filename, mode="rb") as file:
            with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as file_data:
                return file_data.read()

    @staticmethod
    def get_files_to_process() -> List[str]:
        """Returns list of supported files in current directory"""
        return [
            filename for filename in os.listdir()
            if any(filename.endswith(ext) for ext in Config.INCLUDED_EXTENSIONS)
        ]

class ImageProcessor:
    """Handles image processing and effect application"""
    
    def __init__(self, config: Config):
        self.config = config

    def calculate_dimensions(self, data_length: int) -> int:
        """Calculates square image dimensions needed for data"""
        return int(ceil(sqrt(data_length / self.config.BYTES_PER_PIXEL)))

    def get_rgb_values(self, file_data: bytes, start_index: int, color_mode: ColorMode) -> Tuple[int, int, int]:
        """Extracts and processes RGB values based on color mode"""
        r = file_data[start_index] if start_index < len(file_data) else 0
        g = file_data[start_index + 1] if start_index + 1 < len(file_data) else 0
        b = file_data[start_index + 2] if start_index + 2 < len(file_data) else 0
        
        return self._apply_color_mode(r, g, b, color_mode)

    def _apply_color_mode(self, r: int, g: int, b: int, color_mode: ColorMode) -> Tuple[int, int, int]:
        """Applies color transformations based on selected mode"""
        if color_mode == ColorMode.GRAYSCALE:
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            return (gray, gray, gray)
        elif color_mode == ColorMode.SEPIA:
            tr = min(int(0.393 * r + 0.769 * g + 0.189 * b), 255)
            tg = min(int(0.349 * r + 0.686 * g + 0.168 * b), 255)
            tb = min(int(0.272 * r + 0.534 * g + 0.131 * b), 255)
            return (tr, tg, tb)
        elif color_mode == ColorMode.NEON:
            return (
                int(min(r * 1.5, 255)),
                int(min(g * 1.5, 255)),
                int(min(b * 1.5, 255))
            )
        elif color_mode == ColorMode.PASTEL:
            return (
                int((r + 255) / 2),
                int((g + 255) / 2),
                int((b + 255) / 2)
            )
        elif color_mode == ColorMode.AMPLIFIED:
            r = int((r / 128) ** 2 * 255)
            g = int((g / 128) ** 2 * 255)
            b = int((b / 128) ** 2 * 255)
        elif color_mode == ColorMode.COMPLEMENT:
            r = 255 - r
            g = 255 - g
            b = 255 - b
        
        return (r, g, b)

    def create_image(self, file_data: bytes, dimensions: int, effect_style: EffectStyle, color_mode: ColorMode) -> Image.Image:
        """Creates image with specified effects and color mode"""
        output_image = Image.new("RGBA", (dimensions, dimensions), "black")
        
        for x in range(dimensions):
            for y in range(dimensions):
                pixel_index = self._calculate_pixel_index(x, y, dimensions, effect_style, len(file_data))
                rgb_values = self.get_rgb_values(file_data, pixel_index, color_mode)
                output_image.putpixel((x, y), rgb_values + (self.config.DEFAULT_ALPHA,))
        
        return output_image

    def _calculate_pixel_index(self, x: int, y: int, dimensions: int, effect_style: EffectStyle, data_length: int) -> int:
        """Calculates pixel index based on effect style"""
        if effect_style == EffectStyle.MIRROR:
            mirror_x = min(x, dimensions - x - 1)
            mirror_y = min(y, dimensions - y - 1)
            return (mirror_x * dimensions + mirror_y) * self.config.BYTES_PER_PIXEL
        elif effect_style == EffectStyle.ROTATE:
            angle = math.atan2(y - dimensions/2, x - dimensions/2)
            distance = math.sqrt((x - dimensions/2)**2 + (y - dimensions/2)**2)
            pixel_index = int((angle * distance) % data_length)
            pixel_index -= pixel_index % self.config.BYTES_PER_PIXEL
        elif effect_style == EffectStyle.KALEIDOSCOPE:
            sector = math.atan2(y - dimensions/2, x - dimensions/2) % (math.pi/4)
            distance = math.sqrt((x - dimensions/2)**2 + (y - dimensions/2)**2)
            pixel_index = int((sector * distance) % data_length)
            pixel_index -= pixel_index % self.config.BYTES_PER_PIXEL
        elif effect_style == EffectStyle.SPIRAL:
            angle = math.atan2(y - dimensions/2, x - dimensions/2)
            distance = math.sqrt((x - dimensions/2)**2 + (y - dimensions/2)**2)
            pixel_index = int((angle + distance/10) * self.config.BYTES_PER_PIXEL) % data_length
        elif effect_style == EffectStyle.WAVES:
            wave = math.sin(x/20) * 10 + math.cos(y/20) * 10
            pixel_index = int((x + y + wave) * self.config.BYTES_PER_PIXEL) % data_length
        elif effect_style == EffectStyle.MOSAIC:
            tile_size = 20
            tx = (x // tile_size) * tile_size
            ty = (y // tile_size) * tile_size
            pixel_index = (tx * dimensions + ty) * self.config.BYTES_PER_PIXEL
        elif effect_style == EffectStyle.FRACTAL:
            scale = 4 * math.pi / dimensions
            cx = (x - dimensions/2) * scale
            cy = (y - dimensions/2) * scale
            pixel_index = int(abs(cx * cy) * self.config.BYTES_PER_PIXEL) % data_length
        else:  # NONE
            pixel_index = (x * dimensions + y) * self.config.BYTES_PER_PIXEL
        
        return pixel_index

    def apply_effects(self, image: Image.Image, args: argparse.Namespace) -> Image.Image:
        """Applies post-processing effects"""
        if args.blur or args.all_effects:
            image = image.filter(ImageFilter.GaussianBlur(radius=self.config.BLUR_RADIUS))
        
        if args.enhance_color or args.all_effects:
            image = ImageEnhance.Color(image).enhance(self.config.COLOR_ENHANCE)
        
        if args.enhance_contrast or args.all_effects:
            image = ImageEnhance.Contrast(image).enhance(self.config.CONTRAST_ENHANCE)
        
        if args.posterize or args.all_effects:
            image = image.quantize(colors=self.config.POSTER_COLORS).convert('RGBA')
        
        return image

class ArtGenerator:
    """Main class for generating abstract art from binary files"""
    
    def __init__(self):
        self.config = Config()
        self.file_handler = FileHandler()
        self.image_processor = ImageProcessor(self.config)
        self.args = self._parse_arguments()

    def _parse_arguments(self) -> argparse.Namespace:
        """Sets up and parses command line arguments"""
        parser = argparse.ArgumentParser(
            description='Convert binary files into abstract art',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py                           # Process files with default settings
  python main.py --color amplified         # Use amplified colors
  python main.py --effect mirror --blur    # Apply mirror effect with blur
  python main.py --all-effects            # Show all available effects
            """
        )
        
        parser.add_argument('--color', 
                           choices=[mode.value for mode in ColorMode],
                           default=ColorMode.NORMAL.value,
                           help='Color processing mode')
        
        parser.add_argument('--effect',
                           choices=[style.value for style in EffectStyle],
                           default=EffectStyle.NONE.value,
                           help='Pattern effect to apply')
        
        parser.add_argument('--blur',
                           action='store_true',
                           help='Apply Gaussian blur effect')
        
        parser.add_argument('--enhance-color',
                           action='store_true',
                           help='Enhance color saturation')
        
        parser.add_argument('--enhance-contrast',
                           action='store_true',
                           help='Enhance image contrast')
        
        parser.add_argument('--all-effects',
                           action='store_true',
                           help='Apply all available effects')
        
        parser.add_argument('--size',
                           type=int,
                           default=self.config.OUTPUT_IMAGE_SIZE,
                           help='Output image size in pixels')
        
        parser.add_argument('--output-dir',
                           type=str,
                           default='.',
                           help='Directory for output files')
        
        parser.add_argument('--format',
                           choices=['PNG', 'JPEG', 'BMP'],
                           default='PNG',
                           help='Output image format')
        
        return parser.parse_args()

    def generate_image(self, filename: str) -> None:
        """Generates art image from binary file"""
        print(f"\nProcessing {filename}...")
        output_filename = self.file_handler.get_output_filename(filename, self.args)
        
        print("  Reading binary data...")
        file_data = self.file_handler.load_file_data(filename)
        
        print("  Calculating dimensions...")
        dimensions = self.image_processor.calculate_dimensions(len(file_data))
        
        print(f"  Creating {dimensions}x{dimensions} image...")
        print(f"  Applying {self.args.effect} effect with {self.args.color} colors...")
        output_image = self.image_processor.create_image(
            file_data, 
            dimensions,
            EffectStyle(self.args.effect),
            ColorMode(self.args.color)
        )
        
        print("  Applying post-processing effects...")
        output_image = self.image_processor.apply_effects(output_image, self.args)
        
        print(f"  Resizing to {self.config.OUTPUT_IMAGE_SIZE}x{self.config.OUTPUT_IMAGE_SIZE}...")
        resized_image = output_image.resize(
            (self.config.OUTPUT_IMAGE_SIZE, self.config.OUTPUT_IMAGE_SIZE), 
            Image.Resampling.BOX
        )
        
        print(f"  Saving as {output_filename}")
        resized_image.save(output_filename, self.args.format)
        print("  Done!")

    def run(self):
        """Main execution method"""
        files = self.file_handler.get_files_to_process()
        
        if not files:
            print(f"\nNo supported files found in the current directory.")
            print(f"Supported file types: {', '.join(self.config.INCLUDED_EXTENSIONS)}")
            return
        
        print(f"\nFound {len(files)} file(s) to process:")
        for file in files:
            print(f"- {file}")
        
        for input_filename in files:
            self.generate_image(input_filename)
        
        print("\nAll files processed successfully!")
        print("Check the current directory for the generated files.")

def main():
    generator = ArtGenerator()
    generator.run()

if __name__ == "__main__":
    main()