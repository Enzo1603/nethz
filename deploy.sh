#!/bin/bash

# Simple smart deploy script for nethz Django application
# Usage: ./deploy.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting deployment${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found, creating from template${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file with your values before running again${NC}"
    exit 1
fi

# Detect if we need sudo for docker
DOCKER_CMD="docker compose"
if ! docker info >/dev/null 2>&1; then
    if sudo docker info >/dev/null 2>&1; then
        DOCKER_CMD="sudo docker compose"
        echo -e "${BLUE}⚠️  Using sudo for Docker commands${NC}"
    else
        echo -e "❌ Docker is not available or not running"
        exit 1
    fi
fi

# Check if we need to build
NEED_BUILD=false

# Check if image exists
if ! ${DOCKER_CMD%% compose} images --format "table {{.Repository}}:{{.Tag}}" | grep -q "^nethz:latest"; then
    NEED_BUILD=true
    echo -e "${YELLOW}📦 No image found, will build${NC}"
else
    # Check for changes since last build
    if [ -f ".last_build_hash" ]; then
        CURRENT_HASH=$(find . -name "*.py" -o -name "Dockerfile" -o -name "pyproject.toml" -o -name "uv.lock" -o -name "entrypoint.sh" | grep -v __pycache__ | sort | xargs cat | sha256sum | cut -d' ' -f1)
        LAST_HASH=$(cat .last_build_hash)

        if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
            NEED_BUILD=true
            echo -e "${YELLOW}📝 Changes detected, will rebuild${NC}"
        else
            echo -e "${GREEN}✅ No changes detected, using existing image${NC}"
        fi
    else
        NEED_BUILD=true
        echo -e "${YELLOW}📝 No build history, will build${NC}"
    fi
fi

# Build if needed
if [ "$NEED_BUILD" = true ]; then
    echo -e "${BLUE}🔨 Building image...${NC}"
    ./build.sh latest

    # Save build hash
    find . -name "*.py" -o -name "Dockerfile" -o -name "pyproject.toml" -o -name "uv.lock" -o -name "entrypoint.sh" | grep -v __pycache__ | sort | xargs cat | sha256sum | cut -d' ' -f1 > .last_build_hash
fi

echo -e "${BLUE}🔄 Starting containers...${NC}"
$DOCKER_CMD down
$DOCKER_CMD up -d

echo -e "${BLUE}⏳ Waiting for application...${NC}"
sleep 5

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${GREEN}🌐 Application running at http://localhost:8000${NC}"
echo -e "${BLUE}💡 Commands: $DOCKER_CMD logs -f | $DOCKER_CMD down${NC}"
