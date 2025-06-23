#!/bin/bash
# Development runner script for Tai Chi Flow

echo "Starting Tai Chi Flow in development mode..."
echo "========================================="

# Function to cleanup on exit
cleanup() {
    echo -e "\n\nShutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

# Activate backend virtual environment
echo -e "\nActivating Python backend environment..."
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment already active."
elif [ -f "backend/venv/bin/activate" ]; then
    echo "Activating backend/venv..."
    source "backend/venv/bin/activate"
elif [ -f ".venv/bin/activate" ]; then
    echo "Activating .venv..."
    source ".venv/bin/activate"
else
    echo "ERROR: Could not find a virtual environment to activate."
    echo "Please create one (e.g., 'python -m venv .venv') and install dependencies ('pip install -r backend/requirements.txt')."
    exit 1
fi

# Start backend
echo -e "\nStarting Python backend..."
cd backend

python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Test backend health
curl -s http://127.0.0.1:5000/health > /dev/null
if [ $? -ne 0 ]; then
    echo "Backend failed to start!"
    exit 1
fi

echo "Backend started successfully!"

# Start frontend
echo -e "\nStarting Electron frontend..."
npm start &
FRONTEND_PID=$!

echo -e "\n========================================="
echo "Tai Chi Flow is running!"
echo "Backend: http://127.0.0.1:5000"
echo "Frontend: http://localhost:3000"
echo -e "\nPress Ctrl+C to stop"
echo "========================================="

# Wait for processes
wait