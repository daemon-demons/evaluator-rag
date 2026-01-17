#!/bin/bash

echo "========================================="
echo "Starting ERP Certification Assessment"
echo "========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start Backend Server
echo "1. Starting Backend Server (port 8000)..."
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
echo "   Backend started with PID: $BACKEND_PID"
echo "   Backend URL: http://127.0.0.1:8000"
echo ""

# Wait a moment for backend to start
sleep 2

# Start Frontend Server
echo "2. Starting Frontend Server (port 8080)..."
cd "$SCRIPT_DIR/frontend"
python3 -m http.server 8080 &
FRONTEND_PID=$!
echo "   Frontend started with PID: $FRONTEND_PID"
echo "   Frontend URL: http://localhost:8080"
echo ""

echo "========================================="
echo "Both servers are running!"
echo "========================================="
echo ""
echo "✓ Backend: http://127.0.0.1:8000"
echo "✓ Frontend: http://localhost:8080"
echo ""
echo "Open http://localhost:8080 in your browser"
echo ""
echo "To stop both servers, press Ctrl+C or run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Wait for user interrupt
wait
