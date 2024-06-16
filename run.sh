#!/bin/bash

# Save the current directory as a variable
CURRENT_DIR=$(pwd)

# Open a new terminal window and run the uvicorn server
osascript -e 'tell application "Terminal" to do script "cd '$CURRENT_DIR'/back && pipenv run uvicorn app.main:app --reload"' &

# Open a new terminal window and navigate to the frontend directory to run npm
osascript -e 'tell application "Terminal" to do script "cd '$CURRENT_DIR'/front && npm run dev"'
