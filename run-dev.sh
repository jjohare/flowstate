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

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Backend virtual environment not found. Running setup..."
    cd backend
    python setup.py
    cd ..
fi

# Start backend
echo -e "\nStarting Python backend..."
cd backend
if [ -d "venv/bin" ]; then
    # Unix-like systems
    source venv/bin/activate
else
    # Windows Git Bash
    source venv/Scripts/activate 2>/dev/null || true
fi

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