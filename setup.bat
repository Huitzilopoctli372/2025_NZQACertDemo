#!/bin/bash
set -e

echo "======================================"
echo "NZQA Certificate Generator Setup"
echo "======================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed"
    echo "Please install Docker Desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "[ERROR] Docker is not running"
    echo "Please start Docker Desktop"
    exit 1
fi

echo "[OK] Docker is ready"
echo ""

# Create directories
mkdir -p .streamlit templates output

# Build and start
echo "Building and starting container..."
docker-compose up --build -d

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Access the application at:"
echo "  http://localhost:8501"
echo ""

# Try to open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501
elif command -v open &> /dev/null; then
    open http://localhost:8501
fi