# Bin2Art: Transform Retro Code into Digital Art 🎨

Ever wondered what your favorite retro games and programs would look like as art? Bin2Art transforms vintage binary files into stunning abstract artwork, letting you visualize the digital DNA of classic software in beautiful new ways.

## Digital Archaeology Meets Art

Turn binary artifacts from the golden age of computing into mesmerizing visual patterns. Feed Bin2Art your:
- Classic game ROMs
- Vintage program binaries
- Old disk images
- Retro computer files
- Cassette tape dumps
- Ancient executable files

Watch as forgotten bits and bytes metamorphose into vibrant digital paintings, each unique to the original program's structure and content.

## Features That Make Your Bits Beautiful

### 🎨 Color Transformations
- **Normal**: See raw binary patterns
- **Complement**: Explore inverted digital spaces
- **Neon**: Electrify your old code
- **Sepia**: Give your binaries a vintage look
- **Pastel**: Soften the digital edges
- **Grayscale**: Appreciate the binary basics
- **Amplified**: Make those patterns pop

### ✨ Pattern Effects
- **Mirror**: Create symmetrical binary beauty
- **Kaleidoscope**: Fractal-like code patterns
- **Spiral**: Hypnotic data swirls
- **Waves**: Flowing data streams
- **Mosaic**: Digital tile art
- **Fractal**: Complex code structures
- **Rotate**: Circular binary mandalas

## Example: Advanced Lawnmower Simulator Transformed

![Binary art generated from Advanced Lawnmower Simulator](examples/Advanced%20Lawnmower%20Simulator.png)

This mesmerizing pattern was generated from the binary code of "Advanced Lawnmower Simulator". Every curve and color represents actual code and data from the original program, transformed into an abstract visualization.

## Why Bin2Art?

- **Preserve Digital History**: Give old software new life as art
- **Explore Code Aesthetics**: See the hidden beauty in binary
- **Create Unique Art**: Every program generates distinct patterns
- **Celebrate Retro Computing**: Honor classic software visually
- **Generate Wall Art**: Perfect for decorating your coding space
- **Visualize Data**: See programs in a whole new light

## Get Started

Transform your own piece of computing history into art:

```bash
python bin2art.py --color neon --effect spiral game.rom
```

Ready to turn your digital artifacts into art? Check out our [installation guide](#installation) to begin your journey into binary aesthetics.

## Overview

Bin2Art reads any binary file and interprets its data as RGB color values, creating fascinating abstract patterns. Perfect for:
- Visualizing ROM files
- Creating unique artwork from data
- Exploring binary file structures visually
- Generating abstract wallpapers

## Quick Start

```bash
# Install and run in one minute
git clone https://github.com/yourusername/bin2art.git
cd bin2art
pip install -r requirements.txt
python bin2art.py --color neon --effect spiral example.rom
```

## Features

### Color Modes 🎨
| Mode | Description |
|------|-------------|
| `normal` | Direct RGB mapping |
| `complement` | Inverted colors |
| `amplified` | Enhanced contrast |
| `grayscale` | Monochrome |
| `sepia` | Vintage brown tones |
| `neon` | Bright, vivid colors |
| `pastel` | Soft, muted tones |

### Pattern Effects 🌀
| Effect | Description |
|--------|-------------|
| `mirror` | Symmetrical patterns |
| `rotate` | Circular patterns |
| `kaleidoscope` | Complex symmetry |
| `spiral` | Spiral-based patterns |
| `waves` | Undulating patterns |
| `mosaic` | Tile-like patterns |
| `fractal` | Fractal-like patterns |

### Post-Processing 🎯
- `--blur` - Soft, dreamy effect
- `--enhance-color` - Boost color saturation
- `--enhance-contrast` - Increase contrast
- `--posterize` - Reduce to limited color palette

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Steps
```bash
# Clone repository
git clone https://github.com/yourusername/bin2art.git
cd bin2art

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage Examples

### Basic Usage
```bash
# Process all supported files in current directory
python bin2art.py

# Process specific file
python bin2art.py game.rom
```

### Creative Effects
```bash
# Create neon spiral art
python bin2art.py --color neon --effect spiral input.rom

# Generate vintage-style mirror image
python bin2art.py --color sepia --effect mirror --posterize input.dsk

# Create psychedelic kaleidoscope
python bin2art.py --effect kaleidoscope --enhance-color --blur input.mp3
```

## Supported Formats

| Extension | Description | Common Sources |
|-----------|-------------|----------------|
| `.dsk` | Disk images | Retro computers |
| `.tap` | Tape images | ZX Spectrum |
| `.a26` | Atari ROMs | Atari 2600 |
| `.cdt` | CPC tapes | Amstrad CPC |
| `.rom` | ROM files | Various systems |
| `.mp3` | Audio files | Music/Sound |

## Technical Details

### Output Specifications
- Format: PNG (lossless)
- Resolution: 1920x1920 pixels
- Color depth: 32-bit RGBA
- Location: Same directory as input
- Naming: `inputname.png`

### How It Works
1. Memory-maps binary file for efficient reading
2. Groups bytes into RGB triplets
3. Calculates optimal square dimensions
4. Applies selected color transformations
5. Generates pattern effects
6. Applies post-processing filters
7. Outputs final image

## Troubleshooting

### Common Issues
- **"File not found"**: Ensure file path is correct
- **"Memory error"**: File may be too large, try smaller file
- **"Invalid format"**: Check supported file types

### Performance Tips
- Uses memory mapping for efficient processing
- Large files may take longer to process
- Consider using smaller files for testing

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Credits

- Inspired by binary visualization research
- Built with [Pillow](https://python-pillow.org/) imaging library
- Uses NumPy for efficient calculations


