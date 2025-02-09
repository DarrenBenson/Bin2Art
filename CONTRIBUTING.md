# Contributing to Bin2Art

First off, thank you for considering contributing to Bin2Art! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Questions and Support](#questions-and-support)

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Welcome newcomers
- Be collaborative
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards others

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- pip package manager

### Development Environment Setup

1. Fork the Repository
```bash
git clone https://github.com/yourusername/bin2art.git
cd bin2art
```

2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install Dependencies
```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

4. Verify Setup
```bash
# Run tests to ensure everything is working
python test_bin2art.py
```

## Development Workflow

1. Create a New Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. Make Your Changes
- Write code following style guidelines
- Add tests for new functionality
- Update documentation as needed

3. Test Your Changes
```bash
# Run test suite
python test_bin2art.py

# Test with different parameters
python bin2art.py --color neon --effect spiral test.rom
```

## Submitting Changes

### Bug Reports

When submitting a bug report, please include:

- [ ] Clear bug description
- [ ] Steps to reproduce
- [ ] Expected vs actual behavior
- [ ] Python version
- [ ] Operating system
- [ ] Screenshots (if relevant)
- [ ] Sample file (if possible)

### Feature Requests

When proposing new features:

- [ ] Clear feature description
- [ ] Use case explanation
- [ ] Proposed implementation (optional)
- [ ] Example usage
- [ ] Mock-ups (if relevant)

### Pull Requests

1. Update your fork
```bash
git remote add upstream https://github.com/original/bin2art.git
git fetch upstream
git rebase upstream/main
```

2. Push your changes
```bash
git push origin feature/your-feature-name
```

3. Create Pull Request
- Use a clear PR title
- Reference any related issues
- Include before/after screenshots for visual changes
- Complete the PR template

## Style Guidelines

### Python Code Style

```python
from typing import List, Tuple

def process_data(input_data: bytes, options: dict) -> Tuple[int, List[str]]:
    """
    Process binary data according to specified options.

    Args:
        input_data: Raw binary data to process
        options: Dictionary of processing options

    Returns:
        Tuple containing:
        - Status code (0 for success)
        - List of generated file paths
    
    Raises:
        ValueError: If input_data is empty
        KeyError: If required options are missing
    """
    if not input_data:
        raise ValueError("Input data cannot be empty")
    
    # Implementation
```

### Commit Messages

Structure:
```
<type>: <subject>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

Example:
```
feat: Add wave pattern effect

Implemented new wave pattern effect that creates undulating patterns
in the generated art.

- Added WavePattern class
- Updated CLI with --wave-amplitude option
- Added tests and documentation
- Added example images

Closes #42
```

## Testing Guidelines

### Test Structure
```python
def test_feature():
    """
    Test description explaining what is being tested and why.
    """
    # Setup
    input_data = generate_test_data()
    
    # Execute
    result = process_data(input_data)
    
    # Assert
    assert result.status == 'success'
    assert len(result.output) > 0
```

### Test Coverage
- Unit tests for all new functions
- Integration tests for features
- Edge case testing
- Performance testing for large files

## Documentation

### Required Documentation
- [ ] Function/class docstrings
- [ ] Module documentation
- [ ] README updates
- [ ] Example usage
- [ ] Parameter descriptions
- [ ] Error handling

### Example Documentation
```python
class PatternGenerator:
    """
    Generates artistic patterns from binary data.

    This class provides various methods to transform binary data
    into visual patterns using different algorithms and effects.

    Attributes:
        width: Output image width
        height: Output image height
        mode: Color mode to use
    """
```

## Questions and Support

- Open an issue for bugs or feature requests
- Join our community chat for quick questions
- Check the FAQ in the wiki
- Contact maintainers directly for security issues

## License

By contributing to Bin2Art, you agree that your contributions will be licensed under the MIT License.