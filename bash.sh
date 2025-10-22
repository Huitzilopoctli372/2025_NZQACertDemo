#!/bin/bash

# NZQA Certificate Generator - Automated Setup Script
# This script sets up everything needed to run the demo

set -e  # Exit on any error

echo "======================================"
echo "NZQA Certificate Generator Setup"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if Docker is installed
echo "Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    exit 1
fi
print_success "Docker is installed"

# Check if Docker is running
if ! docker info &> /dev/null; then
    print_error "Docker is not running"
    echo ""
    echo "Please start Docker Desktop and try again"
    exit 1
fi
print_success "Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_info "docker-compose not found, will use 'docker compose' instead"
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
    print_success "docker-compose is available"
fi

echo ""
echo "======================================"
echo "Creating project structure..."
echo "======================================"
echo ""

# Create directories
mkdir -p .streamlit
mkdir -p templates
mkdir -p output

print_success "Created .streamlit directory"
print_success "Created templates directory"
print_success "Created output directory"

# Check if files exist
MISSING_FILES=()

if [ ! -f "Dockerfile" ]; then
    MISSING_FILES+=("Dockerfile")
fi

if [ ! -f "docker-compose.yml" ]; then
    MISSING_FILES+=("docker-compose.yml")
fi

if [ ! -f "requirements.txt" ]; then
    MISSING_FILES+=("requirements.txt")
fi

if [ ! -f "streamlit_app.py" ]; then
    MISSING_FILES+=("streamlit_app.py")
fi

if [ ! -f ".streamlit/config.toml" ]; then
    MISSING_FILES+=(".streamlit/config.toml")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_error "Missing required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please ensure all required files are in the current directory:"
    echo "  - Dockerfile"
    echo "  - docker-compose.yml"
    echo "  - requirements.txt"
    echo "  - streamlit_app.py"
    echo "  - .streamlit/config.toml"
    exit 1
fi

print_success "All required files present"

echo ""
echo "======================================"
echo "Building Docker image..."
echo "======================================"
echo ""

# Build the Docker image
$DOCKER_COMPOSE build

print_success "Docker image built successfully"

echo ""
echo "======================================"
echo "Starting container..."
echo "======================================"
echo ""

# Start the container
$DOCKER_COMPOSE up -d

# Wait for container to be healthy
print_info "Waiting for application to start..."
sleep 5

# Check if container is running
if docker ps | grep -q "nzqa-certificate-demo"; then
    print_success "Container is running"
else
    print_error "Container failed to start"
    echo ""
    echo "Checking logs..."
    $DOCKER_COMPOSE logs
    exit 1
fi

echo ""
echo "======================================"
echo "✓ Setup Complete!"
echo "======================================"
echo ""
echo "Your NZQA Certificate Generator is now running!"
echo ""
echo "Access the application at:"
echo "  ${GREEN}http://localhost:8501${NC}"
echo ""
echo "Useful commands:"
echo "  View logs:         $DOCKER_COMPOSE logs -f"
echo "  Stop application:  $DOCKER_COMPOSE down"
echo "  Restart:           $DOCKER_COMPOSE restart"
echo "  View status:       $DOCKER_COMPOSE ps"
echo ""
echo "Opening browser..."

# Try to open browser (platform-specific)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501
elif command -v open &> /dev/null; then
    open http://localhost:8501
elif command -v start &> /dev/null; then
    start http://localhost:8501
else
    echo "Please manually open: http://localhost:8501"
fi

echo ""
print_info "Press Ctrl+C to stop viewing logs, or run '$DOCKER_COMPOSE down' to stop the container"
echo ""

# Follow logs
$DOCKER_COMPOSE logs -f