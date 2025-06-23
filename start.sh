#!/bin/bash
# Tai Chi Flow Application Startup Script

echo "Starting Tai Chi Flow Application..."
echo "=================================="

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check if Python virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "Activating Python virtual environment..."
    source backend/venv/bin/activate
fi

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "Creating models directory..."
    mkdir -p models
fi

# Start the application
echo "Starting backend server..."
cd backend && python app.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend and Electron..."
cd .. && npm run dev

# Kill backend when frontend exits
kill $BACKEND_PID

echo "Application stopped."