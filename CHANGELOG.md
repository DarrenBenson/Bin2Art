# Changelog

All notable changes to Bin2Art will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-01-18

### Added
- CRT post-processing effects: `--antialias` (edge smoothing), `--scanlines` (authentic spacing), `--retro` (both combined)
- Retro computer colour palettes: gameboy (4-shade green), cpc (Amstrad 27-colour), c64 (Commodore 16-colour), spectrum (ZX 16-colour)
- New effects: hilbert (space-filling curve), radial (mandala-like), horizontal (straight bands), diagonal (45-degree stripes), blocks (chunky 8-bit)
- Example gallery with 6 classic game images (Airwolf, Aliens, Amaurote, Arkanoid, Gauntlet, Xanagrams)
- GitHub Actions CI/CD workflow for automated testing
- Issue templates for bug reports and feature requests
- Pull request template
- Security policy (SECURITY.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- This changelog

### Changed
- Streamlined colour modes from 13 to 7 (kept: normal, amplified, neon, gameboy, cpc, c64, spectrum)
- Streamlined effects from 13 to 7 (kept: none, mosaic, hilbert, radial, horizontal, diagonal, blocks)
- Default output size reduced from 1920 to 1024 pixels
- Image resampling changed from LANCZOS to NEAREST for crisp, blocky 8-bit aesthetic
- Converted file handling to use pathlib instead of os.path
- Renamed LICENSE.md to LICENSE for better GitHub integration
- Updated community files to match standard format

### Removed
- Colour modes: complement, grayscale, sepia, pastel, heatmap, rainbow
- Effects: mirror, rotate, kaleidoscope, spiral, waves, fractal, scatter

### Fixed
- Removed broken test_bin2art.py from repository root
- PNG files now saved with optimise=True for smaller file sizes

## [1.0.0] - 2024-10-29

### Added
- Initial release of Bin2Art
- Binary to image conversion functionality
- Colour modes: normal, complement, amplified, grayscale, sepia, neon, pastel
- Effect styles: mirror, rotate, kaleidoscope, spiral, waves, mosaic, fractal
- Post-processing effects: blur, enhance-colour, enhance-contrast, posterize
- Support for .dsk, .tap, .a26, .cdt, .rom, .mp3 file formats
- Comprehensive test suite
- Documentation (README.md, CONTRIBUTING.md)
