#!/bin/bash
# FRIDAY AI Assistant - Setup Script
# Run: chmod +x setup.sh && ./setup.sh

set -e

echo "=========================================="
echo "  FRIDAY AI Assistant - Setup"
echo "=========================================="

# 1. Create .env from .env.example if not exists
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "[OK] Created .env from .env.example"
        echo "[!] Edit .env and add your API keys before running."
    else
        echo "[ERROR] .env.example not found!"
        exit 1
    fi
else
    echo "[OK] .env already exists"
fi

# 2. Install requirements
echo ""
echo "[*] Installing Python dependencies..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "[ERROR] Python not found!"
    exit 1
fi

# Core requirements (always install)
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r requirements.txt || echo "[WARN] Some requirements failed (may be optional)"

# Optional requirements (best-effort)
echo ""
echo "[*] Installing optional dependencies..."
OPTIONAL_PACKAGES=(
    "speechrecognition"
    "pyaudio"
    "chromadb"
    "edge-tts"
    "keyboard"
    "pyautogui"
    "librosa"
    "selenium"
    "pycryptodome"
    "replicate"
    "pygame"
)
for pkg in "${OPTIONAL_PACKAGES[@]}"; do
    echo "  -> $pkg"
    $PYTHON -m pip install "$pkg" 2>/dev/null || echo "     [SKIPPED]"
done

echo ""
echo "[*] Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run: python main.py"
echo "=========================================="
