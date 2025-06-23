#!/bin/bash
# Tai Chi Flow Application Startup Script

echo "Starting Tai Chi Flow Application..."
echo "=================================="

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install --legacy-peer-deps
fi

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

# Activate Python virtual environment
source backend/venv/bin/activate

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "Creating models directory..."
    mkdir -p models
fi

# Start the application
echo "Starting application..."
npm run dev