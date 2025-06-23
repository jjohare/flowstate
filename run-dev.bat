@echo off
REM Development runner script for Tai Chi Flow (Windows)

echo Starting Tai Chi Flow in development mode...
echo =========================================

REM Check if backend virtual environment exists
if not exist "backend\venv" (
    echo Backend virtual environment not found. Running setup...
    cd backend
    python setup.py
    cd ..
)

REM Start backend in new window
echo.
echo Starting Python backend...
start "Tai Chi Backend" cmd /k "cd backend && venv\Scripts\activate && python app.py"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

REM Test backend health
curl -s http://127.0.0.1:5000/health > nul 2>&1
if errorlevel 1 (
    echo Backend may not have started properly!
    echo Please check the backend window for errors.
) else (
    echo Backend started successfully!
)

REM Start frontend
echo.
echo Starting Electron frontend...
npm start

echo.
echo =========================================
echo Tai Chi Flow shutdown complete.
pause