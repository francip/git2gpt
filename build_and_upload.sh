#!/bin/bash

# Exit on error
set -e

# Clean up previous builds
rm -rf build dist

# Build the package
python setup.py sdist bdist_wheel

# Upload to PyPI
python -m twine upload dist/*
