@echo off

echo Installing backend dependencies
cd back
call pipenv install
cd ..

echo Installing frontend dependencies
cd front
call npm install
cd ..

echo Done