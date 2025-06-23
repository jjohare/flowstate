@echo off
REM Tai Chi Flow Application Startup Script for Windows

echo Starting Tai Chi Flow Application...
echo ==================================

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Check if Python virtual environment exists
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
) else (
    echo Activating Python virtual environment...
    call backend\venv\Scripts\activate
)

REM Check if models directory exists
if not exist "models" (
    echo Creating models directory...
    mkdir models
)

REM Start the application
echo Starting application...
start /B cmd /c "cd backend && python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend and Electron
call npm run dev

echo Application stopped.
pause