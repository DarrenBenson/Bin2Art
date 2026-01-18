# Bin2Art

[![Python Tests](https://github.com/DarrenBenson/Bin2Art/actions/workflows/python-tests.yml/badge.svg)](https://github.com/DarrenBenson/Bin2Art/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Transform binary files into abstract artwork. Bin2Art reads any binary file and interprets its data as RGB colour values, creating unique visual patterns from ROMs, disk images, executables, and other binary data.

![Binary art generated from Advanced Lawnmower Simulator](examples/Advanced%20Lawnmower%20Simulator.png)

## Examples

| Spectrum + Horizontal + Retro | Spectrum + Blocks + Scanlines | CPC + Horizontal |
|:-----------------------------:|:-----------------------------:|:----------------:|
| ![Aliens](examples/Aliens.png) | ![Gauntlet](examples/Gauntlet.png) | ![Arkanoid](examples/Arkanoid.png) |

| C64 + Blocks + Scanlines | Neon + Radial | Neon + Radial |
|:------------------------:|:-------------:|:-------------:|
| ![Amaurote](examples/Amaurote.png) | ![Airwolf](examples/Airwolf.png) | ![Xanagrams](examples/Xanagrams.png) |

## Quick Start

```bash
git clone https://github.com/DarrenBenson/Bin2Art.git
cd Bin2Art
pip install -r requirements.txt

# Place binary files in the directory, then run:
python bin2art.py --color spectrum --effect horizontal --retro
```

## Features

### Colour Modes

| Mode | Description |
|------|-------------|
| `normal` | Direct RGB mapping from bytes |
| `amplified` | Enhanced contrast |
| `neon` | Bright, saturated colours |
| `gameboy` | Classic Game Boy 4-shade green palette |
| `cpc` | Amstrad CPC 27-colour palette |
| `c64` | Commodore 64 16-colour palette |
| `spectrum` | ZX Spectrum 16-colour palette |

### Pattern Effects

| Effect | Description |
|--------|-------------|
| `none` | Linear pixel mapping |
| `mosaic` | Tile-based patterns |
| `hilbert` | Space-filling Hilbert curve mapping |
| `radial` | Concentric circles, mandala-like patterns |
| `horizontal` | Straight horizontal bands |
| `diagonal` | 45-degree diagonal stripes |
| `blocks` | Large chunky pixel blocks |

### Retro Effects

| Option | Description |
|--------|-------------|
| `--antialias` | Pixel art edge smoothing |
| `--scanlines` | CRT-style scanlines (authentic spacing) |
| `--retro` | Both antialias and scanlines |

### Post-Processing

| Option | Description |
|--------|-------------|
| `--blur` | Gaussian blur effect |
| `--enhance-color` | Boost colour saturation |
| `--enhance-contrast` | Increase contrast |
| `--posterize` | Reduce to limited palette |
| `--all-effects` | Apply all post-processing |

### Output Options

| Option | Description | Default |
|--------|-------------|---------|
| `--size` | Output image size in pixels | 1024 |
| `--output-dir` | Directory for output files | Current directory |
| `--format` | Output format (PNG, JPEG, BMP) | PNG |

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
git clone https://github.com/DarrenBenson/Bin2Art.git
cd Bin2Art

# Optional: create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Bin2Art processes all supported files in the current directory:

```bash
# Process all supported files with defaults
python bin2art.py

# Apply colour mode and effect
python bin2art.py --color spectrum --effect horizontal

# Add retro CRT effects (scanlines + antialiasing)
python bin2art.py --color spectrum --effect blocks --retro

# Combine multiple options
python bin2art.py --color c64 --effect blocks --scanlines --posterize

# Custom output settings
python bin2art.py --format JPEG --size 3840 --output-dir ./output
```

## Supported File Types

| Extension | Description |
|-----------|-------------|
| `.dsk` | Disk images (various retro computers) |
| `.tap` | Tape images (ZX Spectrum) |
| `.a26` | Atari 2600 ROMs |
| `.cdt` | Cassette tapes (Amstrad CPC) |
| `.rom` | Generic ROM files |
| `.mp3` | Audio files |

## Output

- **Format**: PNG (default, optimised), JPEG (quality 95), or BMP
- **Resolution**: 1024x1024 pixels (configurable via `--size`)
- **Colour depth**: 32-bit RGBA
- **Location**: Same directory as input (or `--output-dir`)
- **Naming**: `{input_name}.{format}`

## How It Works

1. Memory-maps binary file for efficient reading
2. Groups bytes into RGB triplets
3. Calculates optimal square dimensions
4. Applies colour transformation
5. Generates pattern effect
6. Applies post-processing filters
7. Resizes to output dimensions (NEAREST resampling for crisp pixels)
8. Applies retro effects (antialiasing, scanlines)
9. Saves with format-specific optimisation

## Running Tests

```bash
python run_tests.py
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting pull requests and reporting issues.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

- Built with [Pillow](https://python-pillow.org/) and [NumPy](https://numpy.org/)
