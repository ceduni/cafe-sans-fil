@echo off

echo Starting FastAPI backend
cd back
start pipenv run uvicorn app.main:app --reload
cd ..

echo Starting React frontend
cd front
start npm run dev
cd ..

timeout /t 10 >nul

echo Opening in browser
start http://127.0.0.1:8000/docs#/
start http://localhost:5173/

echo Done
