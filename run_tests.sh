#!/bin/bash

# Docker mein venv nahi chahiye, but local ke liye ye check thik hai
if [ -d "venv" ]; then
    echo "Activating local virtual environment..."
    source venv/bin/activate
fi

echo "Starting Pytest suite..."

# Forcefully checking if pytest-dash is available before running
# Takki humein pata chale ki plugin load hua ya nahi
pytest --webdriver Chrome --headless test_app.py

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "--------------------------------------"
    echo "SUCCESS: All tests passed!"
    echo "--------------------------------------"
    exit 0
else
    echo "--------------------------------------"
    echo "FAILURE: Tests failed with exit code $TEST_EXIT_CODE"
    echo "--------------------------------------"
    exit 1
fi