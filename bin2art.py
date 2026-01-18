#!/usr/bin/env python3

# This program converts binary files (ROMs, disk images, audio files, etc.) into abstract art
# It does this by reading the binary data and converting each 3 bytes into RGB pixel values
# The resulting image is a visual representation of the file's binary structure

import mmap
from pathlib import Path
from numpy import ceil, sqrt
from PIL import Image, ImageFilter, ImageEnhance
from typing import List, Tuple
import math
import argparse
from enum import Enum
from dataclasses import dataclass, field


# Enums for different modes and styles
class ColorMode(Enum):
    """Available color modes for image generation."""

    NORMAL = "normal"  # Direct RGB mapping from bytes
    AMPLIFIED = "amplified"  # Enhanced contrast
    NEON = "neon"  # Bright, saturated colours
    GAMEBOY = "gameboy"  # Classic 4-shade green palette
    CPC = "cpc"  # Amstrad CPC 27-colour palette
    C64 = "c64"  # Commodore 64 16-colour palette
    SPECTRUM = "spectrum"  # ZX Spectrum 16-colour palette


class EffectStyle(Enum):
    """Available effect styles for pattern generation."""

    NONE = "none"  # Linear pixel mapping
    MOSAIC = "mosaic"  # Tile-based patterns
    HILBERT = "hilbert"  # Space-filling curve
    RADIAL = "radial"  # Concentric circles, mandala-like
    HORIZONTAL = "horizontal"  # Straight horizontal bands
    DIAGONAL = "diagonal"  # 45-degree diagonal stripes
    BLOCKS = "blocks"  # Large chunky blocks


@dataclass
class Config:
    """Configuration settings for the art generator.

    Attributes:
        INCLUDED_EXTENSIONS: List of file extensions to process
        OUTPUT_IMAGE_SIZE: Size of output image in pixels
        BYTES_PER_PIXEL: Number of bytes used per pixel
        DEFAULT_ALPHA: Default alpha channel value
        POSTER_COLORS: Number of colors for posterize effect
        BLUR_RADIUS: Radius for Gaussian blur
        COLOR_ENHANCE: Color enhancement factor
        CONTRAST_ENHANCE: Contrast enhancement factor
    """

    INCLUDED_EXTENSIONS: List[str] = field(
        default_factory=lambda: ["dsk", "tap", "a26", "cdt", "rom", "mp3"]
    )
    OUTPUT_IMAGE_SIZE: int = 1024
    BYTES_PER_PIXEL: int = 3
    DEFAULT_ALPHA: int = 255
    POSTER_COLORS: int = 8
    BLUR_RADIUS: float = 2.0
    COLOR_ENHANCE: float = 1.5
    CONTRAST_ENHANCE: float = 1.3


class FileHandler:
    """Handles all file-related operations."""

    def __init__(self, config: Config):
        self.config = config

    def get_output_filename(self, input_filename: str, args: argparse.Namespace) -> str:
        """
        Generate output filename based on input file and arguments.

        Args:
            input_filename: Name of input file
            args: Command line arguments

        Returns:
            String containing output file path
        """
        input_path = Path(input_filename)
        output_path = Path(args.output_dir) / f"{input_path.stem}.{args.format.lower()}"
        return str(output_path)

    def load_file_data(self, filename: str) -> bytes:
        """
        Read binary data using memory mapping for efficiency.

        Args:
            filename: Path to file to read

        Returns:
            Bytes containing file data

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be accessed
        """
        with open(filename, mode="rb") as file:
            with mmap.mmap(
                file.fileno(), length=0, access=mmap.ACCESS_READ
            ) as file_data:
                return file_data.read()

    def get_files_to_process(self) -> List[str]:
        """
        Get list of supported files in current directory.

        Returns:
            List of filenames to process
        """
        return [
            f.name
            for f in Path.cwd().iterdir()
            if f.is_file()
            and any(f.name.endswith(ext) for ext in self.config.INCLUDED_EXTENSIONS)
        ]


class ImageProcessor:
    """Handles image processing and effect application."""

    def __init__(self, config: Config):
        self.config = config

    def calculate_dimensions(self, data_length: int) -> int:
        """Calculates square image dimensions needed for data"""
        return int(ceil(sqrt(data_length / self.config.BYTES_PER_PIXEL)))

    def get_rgb_values(
        self, file_data: bytes, start_index: int, color_mode: ColorMode
    ) -> Tuple[int, int, int]:
        """
        Extract and process RGB values from binary data.

        Args:
            file_data: Binary data to process
            start_index: Starting index in data
            color_mode: Color processing mode to apply

        Returns:
            Tuple of (red, green, blue) values

        Raises:
            IndexError: If start_index is out of range
        """
        r = file_data[start_index] if start_index < len(file_data) else 0
        g = file_data[start_index + 1] if start_index + 1 < len(file_data) else 0
        b = file_data[start_index + 2] if start_index + 2 < len(file_data) else 0

        return self._apply_color_mode(r, g, b, color_mode)

    def _apply_color_mode(
        self, r: int, g: int, b: int, color_mode: ColorMode
    ) -> Tuple[int, int, int]:
        """Applies color transformations based on selected mode"""
        if color_mode == ColorMode.NEON:
            return (
                int(min(r * 1.5, 255)),
                int(min(g * 1.5, 255)),
                int(min(b * 1.5, 255)),
            )
        elif color_mode == ColorMode.AMPLIFIED:
            r = min(int((r / 128) ** 2 * 255), 255)
            g = min(int((g / 128) ** 2 * 255), 255)
            b = min(int((b / 128) ** 2 * 255), 255)
        elif color_mode == ColorMode.GAMEBOY:
            # Classic Game Boy 4-shade green palette
            avg = (r + g + b) // 3
            shades = [
                (15, 56, 15),  # Darkest
                (48, 98, 48),  # Dark
                (139, 172, 15),  # Light
                (155, 188, 15),  # Lightest
            ]
            return shades[avg // 64]
        elif color_mode == ColorMode.CPC:
            # Amstrad CPC inspired - 27 colour palette mapped from RGB
            # Quantize each channel to 3 levels
            levels = [0, 128, 255]
            return (
                levels[r // 86],
                levels[g // 86],
                levels[b // 86],
            )
        elif color_mode == ColorMode.C64:
            # Commodore 64 inspired 16-colour palette
            c64_palette = [
                (0, 0, 0),  # Black
                (255, 255, 255),  # White
                (136, 57, 50),  # Red
                (103, 182, 189),  # Cyan
                (139, 63, 150),  # Purple
                (85, 160, 73),  # Green
                (64, 49, 141),  # Blue
                (191, 206, 114),  # Yellow
                (139, 84, 41),  # Orange
                (87, 66, 0),  # Brown
                (184, 105, 98),  # Light Red
                (80, 80, 80),  # Dark Grey
                (120, 120, 120),  # Grey
                (148, 224, 137),  # Light Green
                (120, 105, 196),  # Light Blue
                (159, 159, 159),  # Light Grey
            ]
            # Map RGB to nearest palette entry
            idx = ((r >> 6) << 2) | ((g >> 6) << 1) | (b >> 7)
            return c64_palette[idx % 16]
        elif color_mode == ColorMode.SPECTRUM:
            # ZX Spectrum bright colours - 8 basic + 8 bright
            spectrum_palette = [
                (0, 0, 0),  # Black
                (0, 0, 215),  # Blue
                (215, 0, 0),  # Red
                (215, 0, 215),  # Magenta
                (0, 215, 0),  # Green
                (0, 215, 215),  # Cyan
                (215, 215, 0),  # Yellow
                (215, 215, 215),  # White
                (0, 0, 0),  # Bright Black
                (0, 0, 255),  # Bright Blue
                (255, 0, 0),  # Bright Red
                (255, 0, 255),  # Bright Magenta
                (0, 255, 0),  # Bright Green
                (0, 255, 255),  # Bright Cyan
                (255, 255, 0),  # Bright Yellow
                (255, 255, 255),  # Bright White
            ]
            # Use high bits to select colour
            idx = ((r >> 5) ^ (g >> 5) ^ (b >> 5)) % 16
            return spectrum_palette[idx]

        return (r, g, b)

    def create_image(
        self,
        file_data: bytes,
        dimensions: int,
        effect: EffectStyle,
        color_mode: ColorMode,
    ) -> Image.Image:
        """
        Create image from binary data with specified effects.

        Args:
            file_data: Binary data to process
            dimensions: Size of output image
            effect: Effect style to apply
            color_mode: Color mode to use

        Returns:
            PIL Image object
        """
        output_image = Image.new("RGBA", (dimensions, dimensions), "black")

        for x in range(dimensions):
            for y in range(dimensions):
                pixel_index = self._calculate_pixel_index(
                    x, y, dimensions, effect, len(file_data)
                )
                rgb_values = self.get_rgb_values(file_data, pixel_index, color_mode)
                output_image.putpixel((x, y), rgb_values + (self.config.DEFAULT_ALPHA,))

        return output_image

    def _calculate_pixel_index(
        self, x: int, y: int, dimensions: int, effect: EffectStyle, data_length: int
    ) -> int:
        """Calculates pixel index based on effect style"""
        if effect == EffectStyle.MOSAIC:
            tile_size = 20
            tx = (x // tile_size) * tile_size
            ty = (y // tile_size) * tile_size
            pixel_index = (tx * dimensions + ty) * self.config.BYTES_PER_PIXEL
        elif effect == EffectStyle.HILBERT:
            # Hilbert curve - keeps nearby bytes visually close
            pixel_index = (
                self._hilbert_index(x, y, dimensions) * self.config.BYTES_PER_PIXEL
            )
            pixel_index = pixel_index % data_length
        elif effect == EffectStyle.RADIAL:
            # Concentric circles from centre - mandala effect
            cx, cy = x - dimensions / 2, y - dimensions / 2
            distance = math.sqrt(cx * cx + cy * cy)
            angle = (math.atan2(cy, cx) + math.pi) / (2 * math.pi)  # 0 to 1
            # Map distance and angle to linear index
            ring = int(distance)
            pos_in_ring = int(angle * max(1, ring * 6))  # More positions in outer rings
            pixel_index = (ring * ring + pos_in_ring) * self.config.BYTES_PER_PIXEL
            pixel_index = pixel_index % data_length
        elif effect == EffectStyle.HORIZONTAL:
            # Horizontal bands - straight striped patterns
            # y determines the band, x determines position within band
            pixel_index = (y * dimensions + x) * self.config.BYTES_PER_PIXEL
            pixel_index = pixel_index % data_length
        elif effect == EffectStyle.DIAGONAL:
            # 45-degree diagonal stripes
            diag = x + y
            pos_in_diag = abs(x - y)
            pixel_index = (
                diag * dimensions + pos_in_diag
            ) * self.config.BYTES_PER_PIXEL
            pixel_index = pixel_index % data_length
        elif effect == EffectStyle.BLOCKS:
            # Large chunky blocks - very 8-bit feel
            block_size = max(8, dimensions // 16)  # Adaptive block size
            bx = (x // block_size) * block_size
            by = (y // block_size) * block_size
            pixel_index = (bx * dimensions + by) * self.config.BYTES_PER_PIXEL
            pixel_index = pixel_index % data_length
        else:  # NONE
            pixel_index = (x * dimensions + y) * self.config.BYTES_PER_PIXEL

        return pixel_index

    def _hilbert_index(self, x: int, y: int, size: int) -> int:
        """Convert (x, y) to Hilbert curve index for given size."""
        # Find the order (power of 2) that fits our size
        order = 1
        while (1 << order) < size:
            order += 1
        n = 1 << order

        # Scale coordinates to fit the Hilbert curve order
        hx = (x * n) // size
        hy = (y * n) // size

        # Convert to Hilbert index
        rx, ry, d = 0, 0, 0
        s = n // 2
        while s > 0:
            rx = 1 if (hx & s) > 0 else 0
            ry = 1 if (hy & s) > 0 else 0
            d += s * s * ((3 * rx) ^ ry)
            # Rotate
            if ry == 0:
                if rx == 1:
                    hx = s - 1 - hx
                    hy = s - 1 - hy
                hx, hy = hy, hx
            s //= 2
        return d

    def apply_effects(
        self, image: Image.Image, args: argparse.Namespace
    ) -> Image.Image:
        """
        Apply post-processing effects to image.

        Args:
            image: Input PIL Image
            args: Command line arguments containing effect options

        Returns:
            Processed PIL Image
        """
        if args.blur or args.all_effects:
            image = image.filter(
                ImageFilter.GaussianBlur(radius=self.config.BLUR_RADIUS)
            )

        if args.enhance_color or args.all_effects:
            image = ImageEnhance.Color(image).enhance(self.config.COLOR_ENHANCE)

        if args.enhance_contrast or args.all_effects:
            image = ImageEnhance.Contrast(image).enhance(self.config.CONTRAST_ENHANCE)

        if args.posterize or args.all_effects:
            image = image.quantize(colors=self.config.POSTER_COLORS).convert("RGBA")

        return image

    def apply_retro_effects(
        self, image: Image.Image, args, original_height: int = None
    ) -> Image.Image:
        """
        Apply retro effects after upscaling (antialias, scanlines).

        These effects work best on the upscaled image where pixels are visible blocks.
        """
        retro = getattr(args, "retro", False)

        if getattr(args, "antialias", False) or retro:
            print("  Applying pixel art antialiasing...")
            image = self._apply_pixel_antialias(image)

        if getattr(args, "scanlines", False) or retro:
            print("  Applying scanline effect...")
            image = self._apply_scanlines(image, original_height)

        return image

    def _apply_scanlines(
        self, image: Image.Image, original_height: int = None
    ) -> Image.Image:
        """
        Apply CRT-style scanline effect.

        Darkens rows to simulate the look of a CRT monitor.
        Spacing matches original pixel height for authenticity.
        """
        pixels = image.load()
        width, height = image.size

        # Calculate scanline spacing based on original resolution
        if original_height and original_height > 0:
            # Match scanlines to original pixel rows
            pixel_height = height / original_height
        else:
            pixel_height = 2  # Fallback to every other row

        # Scanline intensity (0.0 = no effect, 1.0 = fully black lines)
        intensity = 0.4

        for y in range(height):
            # Darken the last row of each original pixel
            pixel_row = int(y / pixel_height)
            row_in_pixel = y - int(pixel_row * pixel_height)

            # Darken bottom portion of each pixel row (simulates CRT gap)
            if row_in_pixel >= pixel_height - 1:
                for x in range(width):
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = (
                        int(r * (1 - intensity)),
                        int(g * (1 - intensity)),
                        int(b * (1 - intensity)),
                        a,
                    )

        return image

    def _apply_pixel_antialias(self, image: Image.Image) -> Image.Image:
        """
        Apply classic pixel art antialiasing.

        Detects high-contrast edges and adds intermediate colour pixels
        to smooth transitions while maintaining the pixelated aesthetic.
        """
        pixels = image.load()
        width, height = image.size
        result = image.copy()
        result_pixels = result.load()

        # Threshold for detecting an edge (colour difference)
        edge_threshold = 64

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                current = pixels[x, y]

                # Get cardinal neighbours
                neighbours = [
                    pixels[x, y - 1],  # up
                    pixels[x, y + 1],  # down
                    pixels[x - 1, y],  # left
                    pixels[x + 1, y],  # right
                ]

                # Get diagonal neighbours for smoother AA
                diagonals = [
                    pixels[x - 1, y - 1],  # top-left
                    pixels[x + 1, y - 1],  # top-right
                    pixels[x - 1, y + 1],  # bottom-left
                    pixels[x + 1, y + 1],  # bottom-right
                ]

                # Calculate colour differences with neighbours
                def colour_diff(c1, c2):
                    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

                # Count high-contrast edges
                edge_count = sum(
                    1 for n in neighbours if colour_diff(current, n) > edge_threshold
                )

                # If this pixel is on an edge (2-3 contrasting neighbours)
                if 1 <= edge_count <= 3:
                    # Blend with similar neighbours only
                    similar = [
                        n
                        for n in neighbours + diagonals
                        if colour_diff(current, n) <= edge_threshold
                    ]

                    if similar:
                        # Weight: 60% current pixel, 40% average of similar neighbours
                        avg_r = sum(n[0] for n in similar) // len(similar)
                        avg_g = sum(n[1] for n in similar) // len(similar)
                        avg_b = sum(n[2] for n in similar) // len(similar)

                        new_r = int(current[0] * 0.6 + avg_r * 0.4)
                        new_g = int(current[1] * 0.6 + avg_g * 0.4)
                        new_b = int(current[2] * 0.6 + avg_b * 0.4)

                        result_pixels[x, y] = (new_r, new_g, new_b, current[3])

        return result


class ArtGenerator:
    """Main class for generating abstract art from binary files"""

    def __init__(self):
        self.config = Config()
        self.file_handler = FileHandler(self.config)
        self.image_processor = ImageProcessor(self.config)
        self.args = self._parse_arguments()

    def _parse_arguments(self) -> argparse.Namespace:
        """Sets up and parses command line arguments"""
        parser = argparse.ArgumentParser(
            description="Convert binary files into abstract art",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py                           # Process files with default settings
  python main.py --color amplified         # Use amplified colors
  python main.py --effect mirror --blur    # Apply mirror effect with blur
  python main.py --all-effects            # Show all available effects
            """,
        )

        parser.add_argument(
            "--color",
            choices=[mode.value for mode in ColorMode],
            default=ColorMode.NORMAL.value,
            help="Color processing mode",
        )

        parser.add_argument(
            "--effect",
            choices=[style.value for style in EffectStyle],
            default=EffectStyle.NONE.value,
            help="Pattern effect to apply",
        )

        parser.add_argument(
            "--blur", action="store_true", help="Apply Gaussian blur effect"
        )

        parser.add_argument(
            "--enhance-color", action="store_true", help="Enhance color saturation"
        )

        parser.add_argument(
            "--enhance-contrast", action="store_true", help="Enhance image contrast"
        )

        parser.add_argument(
            "--posterize",
            action="store_true",
            help="Apply poster effect (reduce colors)",
        )

        parser.add_argument(
            "--antialias",
            action="store_true",
            help="Apply pixel art antialiasing (smooths edges)",
        )

        parser.add_argument(
            "--scanlines",
            action="store_true",
            help="Apply CRT-style scanline effect",
        )

        parser.add_argument(
            "--retro",
            action="store_true",
            help="Apply retro CRT look (scanlines + antialiasing)",
        )

        parser.add_argument(
            "--all-effects", action="store_true", help="Apply all available effects"
        )

        parser.add_argument(
            "--size",
            type=int,
            default=self.config.OUTPUT_IMAGE_SIZE,
            help="Output image size in pixels",
        )

        parser.add_argument(
            "--output-dir", type=str, default=".", help="Directory for output files"
        )

        parser.add_argument(
            "--format",
            choices=["PNG", "JPEG", "BMP"],
            default="PNG",
            help="Output image format",
        )

        return parser.parse_args()

    def generate_image(self, filename: str) -> bool:
        """Generates art image from binary file.

        Args:
            filename: Path to input binary file

        Returns:
            True if successful, False otherwise
        """
        print(f"\nProcessing {filename}...")
        output_filename = self.file_handler.get_output_filename(filename, self.args)

        print("  Reading binary data...")
        try:
            file_data = self.file_handler.load_file_data(filename)
        except FileNotFoundError:
            print(f"  Error: File not found: {filename}")
            return False
        except PermissionError:
            print(f"  Error: Permission denied reading: {filename}")
            return False
        except OSError as e:
            print(f"  Error: Cannot read file {filename}: {e}")
            return False

        print("  Calculating dimensions...")
        dimensions = self.image_processor.calculate_dimensions(len(file_data))

        print(f"  Creating {dimensions}x{dimensions} image...")
        print(f"  Applying {self.args.effect} effect with {self.args.color} colors...")
        output_image = self.image_processor.create_image(
            file_data,
            dimensions,
            EffectStyle(self.args.effect),
            ColorMode(self.args.color),
        )

        print("  Applying post-processing effects...")
        output_image = self.image_processor.apply_effects(output_image, self.args)

        print(
            f"  Resizing to {self.config.OUTPUT_IMAGE_SIZE}x{self.config.OUTPUT_IMAGE_SIZE}..."
        )
        resized_image = output_image.resize(
            (self.config.OUTPUT_IMAGE_SIZE, self.config.OUTPUT_IMAGE_SIZE),
            Image.Resampling.NEAREST,
        )

        # Apply retro effects after upscaling (AA and scanlines work better on larger pixels)
        resized_image = self.image_processor.apply_retro_effects(
            resized_image, self.args, dimensions
        )

        print(f"  Saving as {output_filename}")
        save_kwargs = {"format": self.args.format}
        if self.args.format == "PNG":
            save_kwargs["optimize"] = True
        elif self.args.format == "JPEG":
            save_kwargs["quality"] = 95

        try:
            resized_image.save(output_filename, **save_kwargs)
        except PermissionError:
            print(f"  Error: Permission denied writing: {output_filename}")
            return False
        except OSError as e:
            print(f"  Error: Cannot save file {output_filename}: {e}")
            return False

        print("  Done!")
        return True

    def run(self):
        """Main execution method"""
        files = self.file_handler.get_files_to_process()

        if not files:
            print("\nNo supported files found in the current directory.")
            print(f"Supported file types: {', '.join(self.config.INCLUDED_EXTENSIONS)}")
            return

        print(f"\nFound {len(files)} file(s) to process:")
        for file in files:
            print(f"- {file}")

        success_count = 0
        for input_filename in files:
            if self.generate_image(input_filename):
                success_count += 1

        failed_count = len(files) - success_count
        if failed_count == 0:
            print("\nAll files processed successfully!")
        else:
            print(f"\nProcessed {success_count} file(s), {failed_count} failed.")
        print("Check the current directory for the generated files.")


def main():
    generator = ArtGenerator()
    generator.run()


if __name__ == "__main__":
    main()
