#!/bin/bash

# Financial Agent - Quick Setup Script
# This script automates the setup process

set -e  # Exit on error

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════╗"
echo "║   Financial Agent - Setup Script          ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${BLUE}[1/6] Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "\n${BLUE}[2/6] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${BLUE}[3/6] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "\n${BLUE}[4/6] Upgrading pip...${NC}"
pip install --upgrade pip -q
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install dependencies
echo -e "\n${BLUE}[5/6] Installing dependencies...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Error installing dependencies${NC}"
    exit 1
fi

# Check .env configuration
echo -e "\n${BLUE}[6/6] Checking configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    echo -e "${YELLOW}Creating .env from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    
    echo -e "\n${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}⚠ IMPORTANT: Configure your HuggingFace token${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "1. Get your token from: https://huggingface.co/settings/tokens"
    echo "2. Edit .env file: nano .env"
    echo "3. Replace 'your_huggingface_token_here' with your actual token"
    echo ""
else
    echo -e "${GREEN}✓ .env file exists${NC}"
    
    if grep -q "HF_TOKEN=your_huggingface_token_here" .env || grep -q "HF_TOKEN=$" .env; then
        echo -e "${YELLOW}⚠ HuggingFace token not configured${NC}"
        echo -e "${YELLOW}Edit .env and add your HF_TOKEN${NC}"
    else
        echo -e "${GREEN}✓ HuggingFace token configured${NC}"
    fi
fi

# Create necessary directories
mkdir -p data logs

# Final summary
echo -e "\n${GREEN}"
echo "╔════════════════════════════════════════════╗"
echo "║          Setup Complete! 🎉                ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Activate virtual environment:"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "2. Configure your HuggingFace token in .env"
echo -e "   ${YELLOW}nano .env${NC}"
echo ""
echo "3. Run tests:"
echo -e "   ${YELLOW}python tests/test_tools.py${NC}"
echo ""
echo "4. Try the example:"
echo -e "   ${YELLOW}python examples/basic_usage.py${NC}"
echo ""
echo -e "${BLUE}For more info:${NC}"
echo "  • Read SETUP.md for detailed instructions"
echo "  • Read PROJECT_SUMMARY.md for project overview"
echo "  • Use 'make help' to see available commands"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
