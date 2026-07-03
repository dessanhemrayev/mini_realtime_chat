#!/bin/bash

# Script for running tests with various options

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_help() {
    echo "Usage: ./run_tests.sh [option]"
    echo "Options:"
    echo "  all         - Run all tests with coverage"
    echo "  fast        - Run only fast tests"
    echo "  slow        - Run only slow tests"
    echo "  unit        - Run only unit tests"
    echo "  integration - Run only integration tests"
    echo "  coverage    - Run tests and generate coverage report"
    echo "  watch       - Run tests in watch mode (requires pytest-watch)"
    echo "  help        - Show this help message"
    echo ""
}

# Main
case "${1:-all}" in
    all)
        echo -e "${GREEN}Running all tests with coverage...${NC}"
        pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
        ;;
    fast)
        echo -e "${GREEN}Running fast tests...${NC}"
        pytest tests/ -v -m "not slow" --tb=short
        ;;
    slow)
        echo -e "${GREEN}Running slow tests...${NC}"
        pytest tests/ -v -m "slow" --tb=short
        ;;
    unit)
        echo -e "${GREEN}Running unit tests...${NC}"
        pytest tests/ -v -m "unit" --tb=short
        ;;
    integration)
        echo -e "${GREEN}Running integration tests...${NC}"
        pytest tests/ -v -m "integration" --tb=short
        ;;
    coverage)
        echo -e "${GREEN}Running tests with coverage...${NC}"
        pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml
        echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
        ;;
    watch)
        echo -e "${GREEN}Running tests in watch mode...${NC}"
        ptw tests/ -- -v
        ;;
    help)
        print_help
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        print_help
        exit 1
        ;;
esac
