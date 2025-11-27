#!/bin/bash

# Start the worker in the background
python -m app.worker &

# Start the API server in the foreground
uvicorn app.main:app --host 0.0.0.0 --port $PORT
