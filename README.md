# Bin2Art

Transform binary files into stunning abstract art! This tool creates unique visual patterns by converting binary data into colorful images.

![Binary art generated from Advanced Lawnmower Simulator](examples/Advanced%20Lawnmower%20Simulator.png)

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


