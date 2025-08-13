#!/bin/bash

# Simple build script for Docker image
# Usage: ./build.sh [tag]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

IMAGE_NAME="nethz"
TAG="${1:-latest}"

echo -e "${BLUE}🔨 Building Docker image: ${IMAGE_NAME}:${TAG}${NC}"

# Detect if we need sudo for docker
DOCKER_CMD="docker"
if ! docker info >/dev/null 2>&1; then
    if sudo docker info >/dev/null 2>&1; then
        DOCKER_CMD="sudo docker"
        echo -e "${BLUE}⚠️  Using sudo for Docker commands${NC}"
    else
        echo -e "❌ Docker is not available or not running"
        exit 1
    fi
fi

# Build the Docker image
$DOCKER_CMD build -t "${IMAGE_NAME}:${TAG}" .

echo -e "${GREEN}✅ Build completed: ${IMAGE_NAME}:${TAG}${NC}"
echo -e "${BLUE}💡 Run with: $DOCKER_CMD run -p 8000:8000 --env-file .env ${IMAGE_NAME}:${TAG}${NC}"
