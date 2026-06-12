#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "============================================================"
echo "           Solar Array Calculator - Runner Script           "
echo "============================================================"
echo ""

echo "[1/3] Building Docker container environment..."
docker compose build

echo ""
echo "[2/3] Running comprehensive test suite (pytest)..."
echo "------------------------------------------------------------"
docker compose run --rm app pytest -v
echo "------------------------------------------------------------"

echo ""
echo "[3/3] Running main application with example data..."
echo "------------------------------------------------------------"
docker compose run --rm app python src/__main__.py
echo "------------------------------------------------------------"

echo ""
echo "[SUCCESS] All steps executed successfully!"