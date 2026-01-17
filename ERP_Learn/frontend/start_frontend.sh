#!/bin/bash
cd "$(dirname "$0")"

echo "Starting frontend server..."
echo "Open http://localhost:8080 in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

# Try Python 3 first, then fallback to other options
if command -v python3 &> /dev/null; then
    python3 -m http.server 8080
elif command -v python &> /dev/null; then
    python -m http.server 8080
elif command -v php &> /dev/null; then
    php -S localhost:8080
else
    echo "Error: No suitable server found. Please install Python 3 or PHP."
    echo "Or use a simple HTTP server extension in your browser."
    exit 1
fi
