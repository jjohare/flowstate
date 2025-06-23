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

# Check if backend virtual environment is set up correctly
if [ ! -f "backend/venv/bin/activate" ]; then
    echo "Backend virtual environment not found or is corrupted. Recreating..."
    rm -rf backend/venv
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
    cd ..
fi

# Start frontend and backend
echo -e "\nStarting application..."
npm start

echo -e "\n========================================="
echo "Tai Chi Flow is running!"
echo "Backend: http://127.0.0.1:5000"
echo "Frontend: http://localhost:3000"
echo -e "\nPress Ctrl+C to stop"
echo "========================================="

# Wait for processes
wait