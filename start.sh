#!/bin/bash

# Start the simple worker in the background
python -m app.worker_simple &

# Start the API server in the foreground
uvicorn app.main:app --host 0.0.0.0 --port $PORT
