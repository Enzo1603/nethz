#!/bin/bash

# Simple deploy script for nethz Django application
# Usage: ./deploy.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting local deployment${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${YELLOW}💡 Copy .env.example to .env and configure your environment variables${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file from template${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your actual values before running again${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environment file found${NC}"

# Detect if we need sudo for docker
DOCKER_CMD="docker compose"
if ! docker info >/dev/null 2>&1; then
    if sudo docker info >/dev/null 2>&1; then
        DOCKER_CMD="sudo docker compose"
        echo -e "${YELLOW}⚠️  Using sudo for Docker commands${NC}"
    else
        echo -e "${RED}❌ Docker is not available or not running${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}🔄 Starting local deployment...${NC}"
$DOCKER_CMD down
$DOCKER_CMD up -d --build

echo -e "${BLUE}⏳ Waiting for application to start...${NC}"
sleep 10

# Health check
if $DOCKER_CMD ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo -e "${GREEN}🌐 Application is running at http://localhost:8000${NC}"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo -e "${YELLOW}📋 Checking logs...${NC}"
    $DOCKER_CMD logs --tail=20
    exit 1
fi

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${BLUE}💡 Useful commands:${NC}"
echo -e "  View logs: $DOCKER_CMD logs -f"
echo -e "  Stop application: $DOCKER_CMD down"
echo -e "  Restart application: $DOCKER_CMD restart"
