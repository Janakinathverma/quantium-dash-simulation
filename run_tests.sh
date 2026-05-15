#!/bin/bash

# 1. Activate the virtual environment
# Maan ke chal raha hoon ki tumhara venv 'venv' naam ke folder mein hai
source venv/bin/activate

# 2. Execute the test suite
# Hum '--webdriver Chrome' use kar rahe hain kyunki pichle task mein wahi chala tha
pytest --webdriver Chrome test_app.py

# 3. Capture the exit code of the last command (pytest)
TEST_EXIT_CODE=$?

# 4. Return exit code based on test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Tests Passed! System is stable."
    exit 0
else
    echo "Tests Failed! Check the logs above."
    exit 1
fi