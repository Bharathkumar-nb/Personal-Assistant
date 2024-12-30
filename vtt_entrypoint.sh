#!/bin/bash

# Function to handle termination signals
_term() {
  echo "Caught SIGTERM signal!"
  kill -TERM "$child" 2>/dev/null
}

# Trap termination signals
trap _term SIGTERM

# Start the Python script in the background
python voice_to_text.py &
child=$!
wait "$child"
