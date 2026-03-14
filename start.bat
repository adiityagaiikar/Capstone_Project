@echo off
echo ==============================================
echo   Road Safety AI - Startup Sequence Initiated
echo ==============================================

echo [1/3] Setting up FastAPI Backend...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Installing dependencies (this may take a minute)...
pip install -r requirements.txt
echo Starting FastAPI Engine...
start "Road Safety API (Backend)" cmd /k "call venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo [2/3] Setting up React Frontend...
cd ..\frontend\road-safety-ui
echo Starting Vite Development Server...
start "Road Safety UI (Frontend)" cmd /k "npm run dev"

echo [3/3] Online!
echo Both servers are now running in separate windows.
echo Keep those windows open to view live logs.
pause
