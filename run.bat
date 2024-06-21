@echo off
echo Starting FastAPI backend...
cd back
start pipenv run uvicorn app.main:app --reload

echo Starting React frontend...
cd ..
cd front
start npm run dev

echo Both FastAPI and React have been started.
pause
