#!/bin/bash

# Simple build script for local development
# Usage: ./build.sh [--tag custom-tag]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CUSTOM_TAG=""
IMAGE_NAME="nethz"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --tag)
            CUSTOM_TAG="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--tag custom-tag]"
            echo "  --tag TAG       Use custom tag (default: uses pyproject.toml version)"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}🔨 Building Docker image locally${NC}"

# Function to extract version from pyproject.toml without uv
get_version_from_toml() {
    if [ -f "pyproject.toml" ]; then
        # Use Python to parse TOML without external dependencies
        python3 -c "
import re
with open('pyproject.toml', 'r') as f:
    content = f.read()
    match = re.search(r'version\s*=\s*[\"\'](.*?)[\"\']', content)
    if match:
        print(match.group(1))
    else:
        print('unknown')
" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# Generate version tag if not provided
if [ -z "$CUSTOM_TAG" ]; then
    # Try to get version from pyproject.toml
    BASE_VERSION=$(get_version_from_toml)

    if [ "$BASE_VERSION" != "unknown" ]; then
        if git rev-parse --git-dir > /dev/null 2>&1; then
            SHORT_SHA=$(git rev-parse --short HEAD)
            VERSION="${BASE_VERSION}-local.${SHORT_SHA}"
        else
            VERSION="${BASE_VERSION}-local"
        fi
    else
        echo -e "${YELLOW}⚠️  Could not read version from pyproject.toml, using timestamp${NC}"
        VERSION="local-$(date +%H%M%S)"
    fi
    TAG="${IMAGE_NAME}:${VERSION}"
else
    TAG="${IMAGE_NAME}:${CUSTOM_TAG}"
fi

echo -e "${BLUE}📦 Building image: ${TAG}${NC}"

# Detect if we need sudo for docker
DOCKER_CMD="docker"
if ! docker info >/dev/null 2>&1; then
    if sudo docker info >/dev/null 2>&1; then
        DOCKER_CMD="sudo docker"
        echo -e "${YELLOW}⚠️  Using sudo for Docker commands${NC}"
    else
        echo -e "${RED}❌ Docker is not available or not running${NC}"
        exit 1
    fi
fi

# Build the Docker image
$DOCKER_CMD build -t "$TAG" .

echo -e "${GREEN}✅ Image built successfully: ${TAG}${NC}"

# Test the image (simple check that uv and python work)
echo -e "${BLUE}🧪 Testing image...${NC}"
if $DOCKER_CMD run --rm --entrypoint="" "$TAG" uv --version >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Image test passed!${NC}"
else
    echo -e "${RED}❌ Image test failed!${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Build completed!${NC}"
echo -e "${BLUE}💡 Run locally:${NC}"
echo -e "  mkdir -p db"
echo -e "  $DOCKER_CMD run -p 8000:8000 --env-file .env -v \$(pwd)/db:/app/db ${TAG}"
echo -e "${YELLOW}💡 Or use deploy script for easier setup:${NC}"
echo -e "  ./deploy.sh"
