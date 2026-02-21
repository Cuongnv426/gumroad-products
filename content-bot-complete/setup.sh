#!/bin/bash

# Content Bot Setup Script
# Installs dependencies, configures environment, and sets up for deployment

set -e

echo "=================================="
echo "Content Bot - Setup Script"
echo "=================================="
echo ""

# Check Python
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi
python_version=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $python_version found"

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate venv and install dependencies
echo "[3/5] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Create .env file
echo "[4/5] Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created"
    echo "  NOTE: Edit .env and add your API keys!"
else
    echo "✓ .env file already exists"
fi

# Create log directory
echo "[5/5] Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p templates
chmod +x src/bot_main.py
echo "✓ Directories created"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run tests: python src/bot_main.py test"
echo "3. Start bot: python src/bot_main.py start"
echo ""
echo "For VPS deployment:"
echo "  sudo systemctl enable content-bot"
echo "  sudo systemctl start content-bot"
echo ""
