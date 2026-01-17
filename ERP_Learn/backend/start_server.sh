#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate

# Use venv Python explicitly to ensure subprocesses use it too
export PYTHON=$(which python3)
exec python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
