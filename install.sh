#!/bin/bash
# Quick install script for YouTube Channel Corpus Analyzer
# Usage: curl -sL https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/install.sh | bash

set -e

echo "Installing YouTube Channel Corpus Analyzer..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
MIN_VERSION="3.11"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "Error: Python $MIN_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/requirements.txt

# Clone repository (optional, for running locally)
read -p "Clone repository to current directory? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git clone https://github.com/crichalchemist/yt-analysis.git
    cd yt-analysis
    echo ""
    echo "Installation complete!"
    echo "Set your API key: export ANTHROPIC_API_KEY='your_key_here'"
    echo "Run with: python main.py 'https://www.youtube.com/@channel' ./output"
else
    # Download individual files for minimal install
    mkdir -p yt-analysis
    cd yt-analysis

    echo "Downloading modules..."
    curl -sLO https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/acquire.py
    curl -sLO https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/index.py
    curl -sLO https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/extract.py
    curl -sLO https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/synthesize.py
    curl -sLO https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/main.py
    curl -sLO https://raw.githubusercontent.com/crichalchemist/yt-analysis/main/mcp_server.py

    echo ""
    echo "Installation complete!"
    echo "Set your API key: export ANTHROPIC_API_KEY='your_key_here'"
    echo "Run with: python main.py 'https://www.youtube.com/@channel' ./output"
fi
