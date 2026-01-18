# Changelog

All notable changes to Bin2Art will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New retro computer colour palettes: gameboy, cpc, c64, spectrum
- New colour modes: heatmap, rainbow
- New pattern effects: hilbert (space-filling curve), radial (mandala), diagonal, blocks, scatter
- GitHub Actions CI/CD workflow for automated testing
- Issue templates for bug reports and feature requests
- Pull request template
- Security policy (SECURITY.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- This changelog

### Changed
- Renamed LICENSE.md to LICENSE for better GitHub integration
- Updated CONTRIBUTING.md with correct test commands
- Changed image resampling from LANCZOS to NEAREST for crisp, blocky 8-bit aesthetic
- Converted file handling to use pathlib instead of os.path
- Added comprehensive error handling for file operations

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
