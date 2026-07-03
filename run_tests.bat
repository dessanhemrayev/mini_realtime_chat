@echo off
REM Script for running tests on Windows

setlocal enabledelayedexpansion

if "%1%"=="" (
    echo Running all tests with coverage...
    pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
) else if "%1%"=="fast" (
    echo Running fast tests...
    pytest tests/ -v -m "not slow" --tb=short
) else if "%1%"=="slow" (
    echo Running slow tests...
    pytest tests/ -v -m "slow" --tb=short
) else if "%1%"=="unit" (
    echo Running unit tests...
    pytest tests/ -v -m "unit" --tb=short
) else if "%1%"=="integration" (
    echo Running integration tests...
    pytest tests/ -v -m "integration" --tb=short
) else if "%1%"=="coverage" (
    echo Running tests with coverage...
    pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml
    echo Coverage report generated in htmlcov/index.html
) else (
    echo Unknown option: %1%
    echo Usage: run_tests.bat [all^|fast^|slow^|unit^|integration^|coverage]
    exit /b 1
)

endlocal
