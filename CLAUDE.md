# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bin2Art transforms binary files (ROMs, disk images, audio files) into abstract artwork by interpreting binary data as RGB colour values. It uses Pillow for image processing and NumPy for calculations.

## Commands

```bash
# Run the tool on supported files in current directory
python bin2art.py

# Apply colour mode and effect
python bin2art.py --color neon --effect spiral

# Run tests
python run_tests.py

# Lint and format
ruff check --fix . && ruff format .
```

## Architecture

**bin2art.py** - Single-file application with four main classes:

- `Config` (dataclass) - Configuration constants (extensions, image size, effect parameters)
- `FileHandler` - File I/O using memory-mapped files and pathlib
- `ImageProcessor` - Image creation and transformations
- `ArtGenerator` - Main orchestrator with CLI parsing and error handling

**Processing pipeline:**
1. Memory-map binary file (with error handling for missing/inaccessible files)
2. Extract bytes as RGB triplets
3. Calculate square dimensions to fit all pixels
4. Apply colour mode transformation
5. Apply effect style (pixel index mapping algorithms)
6. Apply post-processing filters
7. Resize to output size (NEAREST resampling for crisp pixels)
8. Save with format-specific optimisation (PNG: optimise=True, JPEG: quality=95)

**Enums:**
- `ColorMode` - Colour transformation algorithms (normal, amplified, neon, gameboy, cpc, c64, spectrum)
- `EffectStyle` - Pattern generation algorithms (none, mosaic, hilbert, radial, horizontal, diagonal, blocks)

**Retro palettes (ColorMode):**
- `gameboy` - 4-shade green matching original Game Boy LCD
- `cpc` - Amstrad CPC 27-colour hardware palette
- `c64` - Commodore 64 16-colour VIC-II palette
- `spectrum` - ZX Spectrum 16-colour (8 colours x 2 brightness levels)

**Recommended combinations:**
- `--color spectrum --effect horizontal` - Best overall, shows data structure
- `--color spectrum --effect blocks` - Chunky 8-bit aesthetic
- `--color gameboy --effect diagonal` - Nostalgic green stripes

## Dependencies

- Pillow (PIL) - Image creation and manipulation
- NumPy - Dimension calculations

## Supported File Extensions

dsk, tap, a26, cdt, rom, mp3
