#!/bin/bash

# Start the Ollama server in the background
echo "Starting Ollama server..."
ollama serve &

# Wait for the Ollama server to fully start
echo "Waiting for Ollama server to initialize..."
sleep 1 # Adjust if needed based on server initialization time

# Execute the Python script
echo "Running img processing script ..."
python3 python_scripts/process_img.py

# Check if the Python script completed successfully
if [ $? -eq 0 ]; then
    echo "Image processing completed successfully."
else
    echo "Image processing encountered an error." >&2
fi

# Execute the Python script
echo "Running make playlist script..."
python3 python_scripts/make_playlist.py

# Check if the Python script completed successfully
if [ $? -eq 0 ]; then
    echo "Make playlist script completed successfully."
else
    echo "Make playlist script encountered an error." >&2
fi

# Stop the container
echo "All tasks completed. Exiting container..."

exit 0