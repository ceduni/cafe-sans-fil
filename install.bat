@echo off

pip show pipenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pipenv
    pip install pipenv
)

echo Installing backend dependencies
cd back
call pipenv install
cd ..

echo Installing frontend dependencies
cd front
call npm install
cd ..

echo Done