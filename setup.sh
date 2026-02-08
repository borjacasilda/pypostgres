#!/bin/bash

# PyPostgres Setup Script
# This script sets up the development environment for PyPostgres

set -e

echo "=========================================="
echo "PyPostgres Development Setup"
echo "=========================================="

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Install dev dependencies
echo "✓ Installing dev dependencies..."
pip install pytest pytest-cov black flake8 isort mypy

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file..."
    cp .env.example .env
    echo "  Please edit .env with your PostgreSQL credentials"
fi

# Create logs directory
echo "✓ Creating logs directory..."
mkdir -p logs

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your PostgreSQL credentials"
echo "2. Run tests: python -m pytest tests/ -v"
echo "3. Check examples: python examples/basic_examples.py"
echo ""
echo "For more information, see README.md and QUICKSTART.md"
echo ""
